#!/usr/bin/env node
import { chromium } from "playwright";
import fs from "node:fs/promises";

const base = process.env.TASK027_PREVIEW_URL || "http://127.0.0.1:4173";
const path = "/notes/constant-arguments-with-partner/";
const sizes = [390, 768, 901, 1023, 1280, 1440];
const issues = [], reports = [], out = "qa/article01-browser";
await fs.mkdir(out, { recursive: true });
const browser = await chromium.launch({ headless:true });
try {
  for (const width of sizes) {
    const page = await browser.newPage({ viewport:{width,height:width<=768?844:960}, deviceScaleFactor:1, reducedMotion:"reduce" });
    const errors = [];
    page.on("pageerror", err => errors.push(err.message));
    page.on("console", msg => { if(msg.type()==="error") errors.push(msg.text()); });
    let response;
    try { response = await page.goto(base+path,{waitUntil:"networkidle",timeout:45000}); }
    catch(e) { issues.push(width+": cannot open preview: "+e.message); await page.close(); continue; }
    await page.evaluate(()=>document.fonts?.ready);
    const status = response?.status()||0;
    const r = await page.evaluate(()=>{
      const hero=document.querySelector(".article-hero-visual");
      const img=hero?.querySelector("img");
      const g=document.querySelector(".article-hero-grid");
      const grid=g?getComputedStyle(g).gridTemplateColumns:"";
      const copyRect=document.querySelector(".article-hero-copy")?.getBoundingClientRect();
      const rect=hero?.getBoundingClientRect();
      const docs=document.documentElement;
      const cycle=document.querySelector(".conflict-cycle");
      const lis=cycle?[...cycle.querySelectorAll(":scope > li")]:[];
      const faqs=[...document.querySelectorAll("details.article-qa")];
      const missing=[...document.images].filter(x=>!x.complete||x.naturalWidth===0).map(x=>x.src);
      return {title:document.title,lang:document.documentElement.lang,h1:[...document.querySelectorAll("h1")].map(x=>x.textContent.trim()),canonical:document.querySelector('link[rel="canonical"]')?.href,hreflang:[...document.querySelectorAll('link[rel="alternate"][hreflang]')].map(x=>x.hreflang),heroRatio:rect?rect.width/rect.height:null,heroImg:{complete:img?.complete,naturalWidth:img?.naturalWidth,naturalHeight:img?.naturalHeight,objectFit:img?getComputedStyle(img).objectFit:null},heroGrid:grid,copyRect:copyRect?{left:copyRect.left,right:copyRect.right,top:copyRect.top,bottom:copyRect.bottom,width:copyRect.width}:null,heroRect:rect?{left:rect.left,right:rect.right,top:rect.top,bottom:rect.bottom,width:rect.width}:null,cycleCount:lis.length,faqCount:faqs.length,docWidth:docs.scrollWidth,bodyWidth:document.body.scrollWidth,missingImages:missing,
       noteLinks:[...document.querySelectorAll(".article-toc a")].every(x=>document.getElementById(decodeURIComponent(x.hash.slice(1)))),
       articleCTA:[...document.querySelectorAll('a[href*="consultations/"]')].length};
    });
    const rules=[
      [status===200,"Article HTTP "+status],
      [r.lang==="uk","Incorrect language "+r.lang],
      [r.h1.length===1,"H1 count "+r.h1.length],
      [r.cycleCount===5,"Conflict cycle steps "+r.cycleCount],
      [r.faqCount===4,"FAQ count "+r.faqCount],
      [r.hreflang.length===0,"Unpaired hreflang published"],
      [r.heroImg.complete&&r.heroImg.naturalWidth===1200&&r.heroImg.naturalHeight===900,"Hero not loaded"],
      [r.heroImg.objectFit==="cover","Hero object-fit incorrect"],
      [r.heroRatio&&Math.abs(r.heroRatio-4/3)<0.025,"Hero ratio "+r.heroRatio],
      [r.docWidth<=width+1&&r.bodyWidth<=width+1,"Horizontal scrolling: "+r.docWidth+"/"+r.bodyWidth],
      [r.noteLinks,"Broken TOC anchors"],
      [r.articleCTA>0,"Missing article consultation link"],
      [r.missingImages.length===0,"Broken images: "+r.missingImages.join(" ")],
      [errors.length===0,"Browser errors: "+errors.join(" | ")],
      [(width<=1100 ? r.heroRect?.top >= r.copyRect?.bottom-5 : r.heroRect?.left >= r.copyRect?.right-5 && r.copyRect?.width>=275 && r.heroRect?.width>=275),"Hero geometry at "+width+"px: "+JSON.stringify({grid:r.heroGrid,hero:r.heroRect,copy:r.copyRect})]
    ];
    for (const [ok,why] of rules) if(!ok)issues.push(width+": "+why);
    const toggle=page.locator('[data-menu-toggle]');
    if(width<=1100 && await toggle.isVisible()){
      await toggle.click(); const opened=await toggle.getAttribute("aria-expanded");
      if(opened!=="true")issues.push(width+": mobile menu failed to open");
      await toggle.click();const closed=await toggle.getAttribute("aria-expanded");
      if(closed!=="false")issues.push(width+": mobile menu failed to close");
    }
    await page.screenshot({path:out+"/"+width+"-article.png",fullPage:true});
    reports.push({width,status,...r,errors});
    await page.close();
  }
  const cards=await browser.newPage();
  for(const route of ["/notes/","/"]){
    const resp=await cards.goto(base+route,{waitUntil:"domcontentloaded",timeout:45000});
    const count=await cards.locator('a[href*="constant-arguments-with-partner/"]').count();
    if(resp?.status()!==200||count<1)issues.push("UA "+route+" teaser missing or not served: "+resp?.status()+" links "+count);
  }
  await cards.close();
}finally{await browser.close();}
await fs.writeFile(out+"/report.json",JSON.stringify({base,sizes,reports,issues},null,2));
await fs.writeFile(out+"/report.txt",["TASK 027 article 01 external Owner Preview Chromium audit", "Preview: "+base, "Widths: "+sizes.join(", "), ...issues.map(x=>"FAIL: "+x), issues.length?"FAIL":"PASS"].join("\n"));
console.log("TASK027 Chrome QA: "+(issues.length?"FAIL "+issues.length: "PASS all six sizes"));
for(const issue of issues)console.error(issue);
if(issues.length)process.exit(1);

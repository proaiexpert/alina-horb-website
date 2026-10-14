#!/usr/bin/env node
/* TASK 028 — actual external Chrome owner-preview audit, including phone landscape reading mode */
import { chromium } from "playwright";
import fs from "node:fs/promises";
import path from "node:path";

const ORIGIN = process.env.TASK028_PREVIEW_URL || "https://alina-horb-article01-owner-preview-hga0rv1ln.vercel.app";
const ARTICLE = "/notes/constant-arguments-with-partner/";
const OUTPUT = process.env.TASK028_QA_DIR || "qa/article01-premium-v2";
const VIEWPORTS = [
 { name:"iphone-small", width:375, height:812 },
 { name:"iphone", width:390, height:844 },
 { name:"landscape-phone", width:844, height:390 },
 { name:"landscape-large", width:932, height:430 },
 { name:"tablet-portrait", width:768, height:1024 },
 { name:"tablet-landscape", width:1023, height:768 },
 { name:"desktop", width:1280, height:800 },
 { name:"desktop-wide", width:1440, height:900 }
];
const failures=[], records=[];
const bad=(vp,msg)=>failures.push(`[${vp}] ${msg}`);
await fs.mkdir(OUTPUT,{recursive:true});
const browser=await chromium.launch({headless:true});

async function headerState(page) {
 return page.evaluate(()=>{
  const h=document.querySelector(".site-header--canonical.inner-page-header");
  const el=h?.getBoundingClientRect();
  return {
   exists:Boolean(h), bottom:el?.bottom, top:el?.top,
   hidden:h?.classList.contains("is-reading-hidden"),
   inert:h?.hasAttribute("inert"), ariaHidden:h?.getAttribute("aria-hidden"),
   visibility:h?getComputedStyle(h).visibility:null,
   pointerEvents:h?getComputedStyle(h).pointerEvents:null,
   transform:h?getComputedStyle(h).transform:null,
   height:el?.height,
   menuOpen:document.body.classList.contains("editorial-menu-open")
  };
 });
}
try {
 for(const spec of VIEWPORTS) {
  const isMobile=spec.width<=1180;
  const page=await browser.newPage({viewport:{width:spec.width,height:spec.height},deviceScaleFactor:1,reducedMotion:"no-preference"});
  const errors=[];
  page.on("pageerror",e=>errors.push("pageerror "+e.message));
  page.on("console",m=>{if(m.type()==="error")errors.push("console "+m.text())});
  let response;
  try{response=await page.goto(ORIGIN+ARTICLE,{waitUntil:"networkidle",timeout:50000})}
  catch(e){bad(spec.name,"Navigation "+e.message);await page.close();continue}
  await page.evaluate(()=>document.fonts?.ready);
  // Verify lazy-loaded author portrait only AFTER it has entered viewport.
  // Its normal 'loading=lazy' is intentional and is not a broken image.
  const authorImg=page.locator(".article-author-portrait img");
  await authorImg.scrollIntoViewIfNeeded();
  await authorImg.evaluate(async img => {
    if (!img.complete) await new Promise(resolve => { img.addEventListener("load",resolve,{once:true}); img.addEventListener("error",resolve,{once:true}); setTimeout(resolve,3500); });
    try { await img.decode(); } catch {}
  });
  await page.evaluate(()=>window.scrollTo({top:0,behavior:"instant"}));
  await page.waitForTimeout(300);
  const metrics=await page.evaluate(()=>{
    const img=document.querySelector(".article-hero-visual img");
    const author=document.querySelector(".article-author-portrait img");
    const hero=document.querySelector(".article-hero-visual");
    const hr=hero?.getBoundingClientRect();
    const heroCopy=document.querySelector(".article-hero-copy")?.getBoundingClientRect();
    const body=document.querySelector(".article-body");
    const sectionCount=body?.querySelectorAll("section[id]").length||0;
    const missingImages=[...document.images].filter(i=>!i.complete || i.naturalWidth===0).map(i=>i.currentSrc||i.src);
    return {
      lang:document.documentElement.lang,
      title:document.title,
      h1:[...document.querySelectorAll("h1")].map(x=>x.textContent.trim()),
      docWidth:document.documentElement.scrollWidth,bodyWidth:document.body.scrollWidth,
      heroRatio:hr?hr.width/hr.height:null,
      heroNatural:[img?.naturalWidth,img?.naturalHeight],
      heroFit:img?getComputedStyle(img).objectFit:null,
      authorNatural:[author?.naturalWidth,author?.naturalHeight],
      authorAlt:author?.alt,
      authorLabel:document.querySelector(".article-author-qualification")?.textContent.trim(),
      faqCount:document.querySelectorAll(".article-qa").length,
      stages:document.querySelectorAll(".conflict-cycle > li").length,
      recurrence:!!document.querySelector(".conflict-recurrence"),
      sectionCount,
      hasCTA:!!document.querySelector(".article-conclusion-action a[href*='consultations/']"),
      hrefs:[...document.querySelectorAll(".article-toc a[href^='#']")].every(a=>document.getElementById(decodeURIComponent(a.hash.slice(1)))),
      heroGeometry: {imageX:hr?.left,copyRight:heroCopy?.right, imageY:hr?.top,copyBottom:heroCopy?.bottom},
      missingImages
    };
  });
  const initial=await headerState(page);
  if(response?.status()!==200)bad(spec.name,"Article HTTP "+response?.status());
  if(metrics.lang!=="uk"||metrics.h1.length!==1)bad(spec.name,"Unexpected language or H1");
  if(metrics.docWidth>spec.width+1||metrics.bodyWidth>spec.width+1)bad(spec.name,`Horizontal overflow ${metrics.docWidth}/${metrics.bodyWidth}`);
  if(!metrics.heroRatio||Math.abs(metrics.heroRatio-4/3)>.03)bad(spec.name,"Hero not 4:3");
  if(metrics.heroNatural.join(",")!=="1200,900"||metrics.heroFit!=="cover")bad(spec.name,"Hero size/crop regression");
  if(metrics.authorNatural[0]<400||metrics.authorNatural[1]<400)bad(spec.name,"Verified author photo missing");
  if(metrics.authorLabel!=="Психолог · Магістр психології")bad(spec.name,"Author credentials incorrect");
  if(metrics.faqCount!==4||metrics.stages!==5||!metrics.recurrence)bad(spec.name,"Four FAQs / five stages / optional recurrence broken");
  if(metrics.sectionCount!==12||!metrics.hasCTA||!metrics.hrefs)bad(spec.name,"Content sections/CTA/anchors broken");
  if(metrics.missingImages.length)bad(spec.name,"Broken images: "+metrics.missingImages.join("; "));
  if(initial.hidden||initial.inert||initial.ariaHidden)bad(spec.name,"Header not visible initially");
  if(spec.width<=1100&&metrics.heroGeometry.imageY<metrics.heroGeometry.copyBottom-6)bad(spec.name,"Mobile/tablet Hero is not text-then-image");
  if(spec.width>1180&&metrics.heroGeometry.imageX<metrics.heroGeometry.copyRight-6)bad(spec.name,"Desktop Hero overlaps editorial text");

  const screenshot=async suffix=>page.screenshot({path:path.join(OUTPUT,`${spec.name}-${suffix}.png`),fullPage:suffix==="full"});
  if([375,844,932,1440].includes(spec.width))await screenshot("initial");
  await screenshot("full");

  const headerEvents={initial};
  if(isMobile){
    // Trigger genuine scroll events inside article; header should hide without shifting the document.
    await page.evaluate(()=>{
      const el=document.querySelector(".article-body");
      const y=Math.max(450,window.scrollY + el.getBoundingClientRect().top+190);
      window.scrollTo({top:y,behavior:"instant"});
    });
    await page.waitForTimeout(430);
    const down=await headerState(page);headerEvents.down=down;
    const after=await page.evaluate(()=>({y:window.scrollY,docWidth:document.documentElement.scrollWidth}));
    if(!down.hidden||!down.inert||down.ariaHidden!=="true"||down.pointerEvents!=="none")
      bad(spec.name,"Reading header did not become fully hidden/inert "+JSON.stringify(down));
    if(down.bottom>1)bad(spec.name,"Hidden header still obstructs viewport: bottom "+down.bottom);
    if(after.docWidth>spec.width+1)bad(spec.name,"Header transition caused overflow");
    if([375,844,932].includes(spec.width))await screenshot("header-hidden");

    // Small upward gesture should reopen after direction threshold.
    await page.evaluate(()=>window.scrollBy({top:-180,behavior:"instant"}));
    await page.waitForTimeout(430);
    const up=await headerState(page);headerEvents.up=up;
    if(up.hidden||up.inert||up.ariaHidden)bad(spec.name,"Header did not reopen on upward scroll");
    if([375,844,932].includes(spec.width))await screenshot("header-restored");

    // Opening menu must keep header visible and preserve close/Escape behavior.
    const toggle=page.locator("[data-menu-toggle]");
    if(!await toggle.isVisible())bad(spec.name,"Navigation toggle missing");
    else{
      await toggle.click();await page.waitForTimeout(160);
      const menuOpen=await headerState(page);headerEvents.menuOpen=menuOpen;
      if(!menuOpen.menuOpen||menuOpen.hidden||menuOpen.inert)bad(spec.name,"Open menu suppresses header");
      if(await toggle.getAttribute("aria-expanded")!=="true")bad(spec.name,"Menu aria-expanded did not open");
      if([844,932].includes(spec.width))await screenshot("menu-open");
      await page.keyboard.press("Escape");await page.waitForTimeout(190);
      const closed=await headerState(page);
      if(closed.menuOpen||(await toggle.getAttribute("aria-expanded"))!=="false")bad(spec.name,"Escape did not close drawer");
    }

    // Header focus must remain possible when visible, and hidden links must be inert.
    await page.evaluate(()=>window.scrollTo({top:0,behavior:"instant"}));await page.waitForTimeout(300);
    const hLink=page.locator(".site-header a").first();
    await hLink.focus();
    const focused=await page.evaluate(()=>document.querySelector(".site-header")?.contains(document.activeElement));
    if(!focused)bad(spec.name,"Visible header is not keyboard focusable");
    await page.evaluate(()=>document.activeElement.blur());
    // Reading mode intentionally allows an anchor/focus safety period of 950ms.
    await page.waitForTimeout(1050);
    await page.evaluate(()=>window.scrollTo({top:document.querySelector(".article-body").offsetTop+240,behavior:"instant"}));
    await page.waitForTimeout(420);
    const hiddenNow=await headerState(page);
    if(!hiddenNow.hidden)bad(spec.name,"Header failed to re-hide after focus released");
    // TOC hash navigation from a hidden state must restore header and preserve target visibility.
    const toc=page.locator(".article-toc a").first();
    if(await toc.count()){
      await toc.click();await page.waitForTimeout(410);
      const nav=await headerState(page);headerEvents.toc=nav;
      const focusTarget=await page.evaluate(()=>{
        const l=document.querySelector(".article-toc a"),e=document.getElementById(decodeURIComponent(l.hash.slice(1)));
        const r=e?.getBoundingClientRect();return {hash:location.hash,top:r?.top};
      });
      if(!focusTarget.hash||!Number.isFinite(focusTarget.top))bad(spec.name,"TOC navigation failed");
      if(nav.hidden)bad(spec.name,"TOC did not show header");
      await page.goBack({waitUntil:"domcontentloaded",timeout:12000}).catch(()=>null);
      await page.waitForTimeout(260);
      if(await page.locator(".article-body").count()===0)bad(spec.name,"Browser Back lost article");
    }
    if(spec.width===844||spec.width===932){
      await page.setViewportSize({width:spec.height,height:spec.width});
      await page.waitForTimeout(160);
      await page.setViewportSize({width:spec.width,height:spec.height});
      await page.waitForTimeout(250);
      const oriented=await headerState(page);headerEvents.orientation=oriented;
      if(!oriented.exists||oriented.hidden)bad(spec.name,"Orientation change left header hidden");
    }
  } else if(initial.hidden||initial.inert)bad(spec.name,"Desktop header should never be hidden");
  // Native details must allow keyboard activation and retain semantics.
  const summary=page.locator("details.article-qa summary").first();
  await summary.focus();await page.keyboard.press("Enter");
  if(!(await page.locator("details.article-qa").first().getAttribute("open")!==null))bad(spec.name,"FAQ keyboard toggle failed");
  await page.keyboard.press("Enter");
  if(await page.locator("details.article-qa").first().getAttribute("open")!==null)bad(spec.name,"FAQ keyboard close failed");
  if(errors.length)bad(spec.name,"Console/runtime "+errors.join(" | "));
  records.push({viewport:spec,metrics,headerEvents,errors,passed:!failures.some(x=>x.startsWith(`[${spec.name}]`))});
  await page.close();
 }

 const page=await browser.newPage({viewport:{width:390,height:844},reducedMotion:"reduce"});
 await page.goto(ORIGIN+ARTICLE,{waitUntil:"networkidle",timeout:45000});
 const duration=await page.locator(".site-header--canonical.inner-page-header").evaluate(x=>getComputedStyle(x).transitionDuration);
 if(duration.split(",").some(x=>parseFloat(x)>0))bad("reduced-motion","Nonzero header transition: "+duration);
 await page.waitForTimeout(1100);
 await page.evaluate(()=>window.scrollTo({top:document.querySelector(".article-body").offsetTop+200,behavior:"instant"}));
 await page.waitForTimeout(180);
 if(!(await headerState(page)).hidden)bad("reduced-motion","Scrolling did not hide header");
 await page.close();
 for(const route of ["/notes/","/"]){
  const p=await browser.newPage();let res=await p.goto(ORIGIN+route,{waitUntil:"domcontentloaded",timeout:45000});
  const count=await p.locator('a[href*="constant-arguments-with-partner/"]').count();
  if(res?.status()!==200||count===0)bad("teasers",route+" route/card unavailable");
  await p.close();
 }
} finally {await browser.close()}
await fs.writeFile(path.join(OUTPUT,"report.json"),JSON.stringify({origin:ORIGIN,viewports:VIEWPORTS,records,failures},null,2));
await fs.writeFile(path.join(OUTPUT,"report.txt"),[
 "TASK 028 Premium Article V2 / isolated Vercel Chrome",`Preview: ${ORIGIN}`,
 `Pass: ${VIEWPORTS.length}-viewport responsive + interactive header + reduced motion`,
 ...failures.map(x=>"FAIL "+x),failures.length?"FAIL":"PASS"
].join("\n"));
console.log(`TASK028 Owner Preview Chrome QA: ${failures.length?"FAIL "+failures.length:"PASS"}`);
for(const issue of failures)console.error(issue);
if(failures.length)process.exit(1);

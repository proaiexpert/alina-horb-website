#!/usr/bin/env node
/* TASK031: real isolated bilingual preview QA; no publication writes. */
import { chromium } from "playwright";
import fs from "node:fs/promises";
import path from "node:path";
const BASE=process.env.TASK031_PREVIEW_URL || "https://alina-horb-article01-owner-preview-khnf27kps.vercel.app";
const ROUTE="/notes/constant-arguments-with-partner/";
const viewports=[
 ["iphone-small",375,812],["iphone",390,844],["phone-landscape",844,390],
 ["large-landscape",932,430],["tablet-portrait",768,1024],
 ["tablet-landscape",1023,768],["desktop",1280,800],["desktop-wide",1440,900]
];
const output="qa/task031-bilingual";await fs.mkdir(output,{recursive:true});
const errors=[],entries=[],browser=await chromium.launch({headless:true});
const fail=(label,message)=>errors.push(label+": "+message);
const absolute=href=>new URL(href,BASE);
const articleRoute=lang=>lang==="ru"?"/ru"+ROUTE:ROUTE;
const canonical=lang=>"https://alinahorb.com"+articleRoute(lang);
async function menuState(page){return page.evaluate(()=>{
 const header=document.querySelector(".site-header--canonical.inner-page-header");
 return {hidden:header?.classList.contains("is-reading-hidden"),inert:header?.hasAttribute("inert"),
 aria:header?.getAttribute("aria-hidden"),bottom:header?.getBoundingClientRect().bottom,menu:document.body.classList.contains("editorial-menu-open")}
})}
try{
for(const lang of ["uk","ru"]){
for(const [label,width,height] of viewports){
 const id=lang+"-"+label;
 const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1,reducedMotion:"reduce"});
 const jsErrors=[];page.on("pageerror",e=>jsErrors.push(e.message));
 page.on("console",m=>{if(m.type()==="error")jsErrors.push(m.text())});
 const response=await page.goto(BASE+articleRoute(lang),{waitUntil:"networkidle",timeout:60000}).catch(e=>{fail(id,"navigation "+e.message);return null});
 if(!response){await page.close();continue}
 const status=response.status(),header=response.headers()["x-robots-tag"]||"";
 const author=page.locator(".article-author-portrait img");
 await author.scrollIntoViewIfNeeded();
 await author.evaluate(async el=>{try{await el.decode()}catch{}}).catch(()=>{});
 await page.evaluate(()=>window.scrollTo({top:0,behavior:"instant"}));
 await page.waitForTimeout(200);
 const metric=await page.evaluate((pageLang)=>{
   const q=s=>document.querySelector(s),qa=s=>[...document.querySelectorAll(s)];
   const h=q(".article-hero-visual"),hr=h?.getBoundingClientRect(),copy=q(".article-hero-copy")?.getBoundingClientRect();
   const caseItems=qa(".article-case-voice"),caseRects=caseItems.map(el=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}});
   const spans=qa(".conflict-cycle-num").map(el=>{const r=el.getBoundingClientRect();return {label:el.textContent.trim(),center:r.x+r.width/2}});
   const alts=Object.fromEntries(qa('link[hreflang]').map(x=>[x.hreflang,x.href]));
   const graph=JSON.parse(q('script[type="application/ld+json"]').textContent)["@graph"];
   const faq=graph.find(x=>x["@type"]==="FAQPage");
   return {
    lang:document.documentElement.lang,title:document.title,description:q('meta[name="description"]')?.content,
    introFirst:q('.article-essay-intro > p:first-of-type')?.textContent.trim(),
    footerSwitch:qa('footer.site-footer .footer-utility .language-switch a').map(el=>el.href),
    canonical:q('link[rel="canonical"]')?.href,alts,h1:qa("h1").map(x=>x.textContent.trim()),
    width:document.documentElement.scrollWidth,
    hero:{ratio:hr?.width/hr?.height,copyRight:copy?.right,imageLeft:hr?.left,imageTop:hr?.top,copyBottom:copy?.bottom,
    natural:q(".article-hero-visual img")?.naturalWidth},
    author:{natural:q(".article-author-portrait img")?.naturalWidth,name:q("#article01-author-name")?.textContent.trim(),
      credential:q(".article-author-qualification")?.textContent.trim()},
    schema:{types:graph.map(x=>x["@type"]),article:graph.find(x=>x["@type"]==="Article"),
       faq:faq?.mainEntity||[],crumb:graph.find(x=>x["@type"]==="BreadcrumbList")},
    toc:qa(".article-toc a").map(x=>({href:x.href,exists:!!document.getElementById(decodeURIComponent(x.hash.slice(1)))})),
    case:caseItems.map(x=>x.textContent.trim()),caseRects,
    caseFriday:q(".article-case-context")?.textContent.includes(pageLang==="ru"?"вечер пятницы":"вечір п’ятниці"),
    cycle:qa(".conflict-cycle > li").map(x=>({number:x.querySelector(".conflict-cycle-num")?.textContent.trim(),title:x.querySelector("strong")?.textContent.trim(),desc:x.querySelector("p")?.textContent.trim()})),
    stages:spans,spine:getComputedStyle(q(".conflict-cycle"),"::before").backgroundColor,
    recurrence:q(".conflict-recurrence")?.textContent.trim(),
    faqVisible:qa("details.article-qa").map(x=>({q:x.querySelector("summary")?.textContent.trim(),a:x.querySelector("p")?.textContent.trim()})),
    buttons:qa(".article-cta-band--v21 .article-cta-primary").map(x=>({text:x.textContent.trim(),href:x.href})),
    menuVisible:!!q("[data-menu-toggle]"),
    links:qa("a[href]").map(x=>({raw:x.getAttribute("href"),url:x.href})),
    missing:qa("img").filter(x=>!x.complete||x.naturalWidth===0).map(x=>x.src)
   }
 },lang);
 if(status!==200)fail(id,"HTTP "+status);
 if(!header.includes("noindex")||!header.includes("nofollow"))fail(id,"preview indexing guard missing "+header);
 if(metric.lang!==lang)fail(id,"Wrong html lang");
 if(metric.h1.length!==1)fail(id,"H1 count");
 if(metric.width>width+1)fail(id,"Horizontal overflow "+metric.width+" > "+width);
 if(Math.abs(metric.hero.ratio-4/3)>.035||metric.hero.natural!==1200)fail(id,"Hero 4:3/asset");
 if(width<=1100 ? metric.hero.imageTop<metric.hero.copyBottom-7 : metric.hero.imageLeft<metric.hero.copyRight-6)fail(id,"Hero geometry overlap");
 if(metric.author.natural!==900||metric.author.credential!==(lang==="ru"?"Психолог · Магистр психологии":"Психолог · Магістр психології"))fail(id,"Author photo or credential");
 if(metric.cycle.length!==5||metric.stages.map(x=>x.label).join("|")!=="01|02|03|04|05")fail(id,"Five-stage order");
 if(metric.stages.some(x=>Math.abs(x.center-metric.stages[0].center)>3)||metric.spine==="rgba(0, 0, 0, 0)")fail(id,"Unconnected cycle spine");
 if(!metric.recurrence?.includes(lang==="ru"?"не является неизбежным":"не є неминучим"))fail(id,"Optional recurrence missing");
  const expectedIntro=lang==="ru"?"Иногда кажется, что отношения превратились в бесконечное повторение":"Іноді здається, що стосунки перетворилися";
  if(!metric.introFirst?.startsWith(expectedIntro))fail(id,"First approved introductory paragraph is missing");
  if(metric.footerSwitch.length!==1||new URL(metric.footerSwitch[0]).pathname!==new URL(canonical(lang==="ru"?"uk":"ru")).pathname)fail(id,"Footer language switch must link to paired article");
 if(!metric.caseFriday||metric.case.length!==2)fail(id,"Two-voice Friday case invalid");
 if(lang==="ru"&&(!metric.case[0].includes("Для тебя всегда всё важнее меня")||!metric.case[1].includes("Я работаю, чтобы у нас всё было нормально")))fail(id,"RU voices not localized");
 if(lang==="uk"&&(!metric.case[0].includes("Для тебе завжди все важливіше")||!metric.case[1].includes("Я працюю, щоб у нас усе було нормально")))fail(id,"UA voices corrupted");
 if(width<=620?metric.caseRects[0]?.y+metric.caseRects[0]?.h>metric.caseRects[1]?.y+4:Math.abs(metric.caseRects[0]?.y-metric.caseRects[1]?.y)>4)fail(id,"Responsive voice layout");
 if(metric.faqVisible.length!==4||metric.schema.faq.length!==4)fail(id,"Four FAQ parity missing");
 metric.faqVisible.forEach((v,i)=>{if(v.q!==metric.schema.faq[i]?.name||v.a!==metric.schema.faq[i]?.acceptedAnswer?.text)fail(id,"FAQ visible vs JSON-LD mismatch "+i)});
 if(metric.schema.article?.inLanguage!==lang||metric.schema.article?.mainEntityOfPage!==canonical(lang))fail(id,"Article structured-data identity");
 if(!metric.schema.types.includes("BreadcrumbList"))fail(id,"Breadcrumb schema missing");
 if(metric.canonical!==canonical(lang))fail(id,"Canonical mismatch");
 for(const [code,expected] of Object.entries({uk:canonical("uk"),ru:canonical("ru"),"x-default":canonical("uk")}))if(metric.alts[code]!==expected)fail(id,"hreflang "+code);
 if(metric.buttons.length!==1||new URL(metric.buttons[0].href).pathname!=="/"+(lang==="ru"?"ru/":"")+"consultations/")fail(id,"CTA mismatch");
 if(metric.toc.length!==11||metric.toc.some(x=>!x.exists))fail(id,"TOC anchors broken");
 if(metric.missing.length)fail(id,"Missing image "+metric.missing.join(","));
 if(metric.links.some(x=>/^\s*#\s*$/.test(x.raw)||!x.url))fail(id,"Empty link");
 if(jsErrors.length)fail(id,"Console "+jsErrors.join(" ; "));
 const initial=await menuState(page);if(initial.hidden||initial.inert)fail(id,"Header hidden on initial load");
 if(width<=1180){
  await page.evaluate(()=>window.scrollTo({top:0,behavior:"instant"})); await page.waitForTimeout(150);
  for(let k=0;k<7;k++){await page.mouse.wheel(0,270);await page.waitForTimeout(70)}
  await page.waitForTimeout(270);
  let down=await menuState(page);
  if(!down.hidden||!down.inert||down.aria!=="true"||down.bottom>2)fail(id,"Reading header not fully hidden "+JSON.stringify(down));
  await page.mouse.wheel(0,-280);await page.waitForTimeout(350);let up=await menuState(page);
  if(up.hidden||up.inert)fail(id,"Header not revealed on upward gesture");
  const toggle=page.locator("[data-menu-toggle]");
  if(await toggle.isVisible()){
   await toggle.click();await page.waitForTimeout(120);
   let m=await menuState(page);
   if(!m.menu||m.hidden||m.inert)fail(id,"Menu cannot remain open");
   await page.keyboard.press("Escape");await page.waitForTimeout(100);
   if((await menuState(page)).menu)fail(id,"Menu Escape close failed");
  }
  if(label.includes("landscape"))await page.screenshot({path:path.join(output,id+"-landscape.png")});
 }else if(initial.hidden)fail(id,"Unexpected desktop reading mode");
 const first=page.locator("details.article-qa summary").first();
 await first.focus();await page.keyboard.press("Enter");if(await page.locator("details.article-qa").first().getAttribute("open")===null)fail(id,"FAQ keyboard open failed");
 await page.keyboard.press("Enter");if(await page.locator("details.article-qa").first().getAttribute("open")!==null)fail(id,"FAQ keyboard close failed");
 if([390,1440].includes(width)){
  await page.screenshot({path:path.join(output,id+"-full.png"),fullPage:true});
  for(const [query,name] of [[".article-case","case"],[".article-process","process"],[".article-author-card","author"],[".article-cta-band--v21","cta"]])await page.locator(query).screenshot({path:path.join(output,id+"-"+name+".png")});
 }
 const uiSwitch=lang==="ru"?"UA":"RU";
 const switchHref=lang==="ru"?"/notes/constant-arguments-with-partner/":"/ru/notes/constant-arguments-with-partner/";
 const languageAnchor=page.locator("header.site-header .language-switch a");
 const loc=await languageAnchor.getAttribute("href");
 if(new URL(loc,BASE+articleRoute(lang)).pathname!==switchHref)fail(id,"Switch destination invalid "+loc);
 if(width===390){
  // The header is intentionally hidden while reading. Scroll up as a user would,
  // then activate the actually visible language switch instead of clicking hidden UI.
  await page.evaluate(()=>window.scrollTo({top:0,behavior:"instant"}));
  await page.waitForTimeout(380);
  if((await menuState(page)).hidden)fail(id,"Header unavailable at top before language switch");
  await languageAnchor.click();await page.waitForLoadState("domcontentloaded");
  if(!page.url().includes(switchHref)||await page.locator("html").getAttribute("lang")==lang)fail(id,"Real click language switch invalid");
 }
 entries.push({id,width,height,metrics:{caseRects:metric.caseRects,stageCount:metric.cycle.length,faqCount:metric.faqVisible.length,meta:metric.canonical,images:metric.missing},jsErrors,failed:errors.filter(x=>x.startsWith(id+":"))});
 await page.close();
}}
 const tab=await browser.newPage({viewport:{width:390,height:844}});
 for(const language of ["uk","ru"]){
  const prefix=language==="ru"?"/ru":"";
  for(const route of ["/notes/","/"]){
   const r=await tab.goto(BASE+prefix+route,{waitUntil:"domcontentloaded",timeout:45000});
   const found=await tab.locator('a[href*="constant-arguments-with-partner/"]').count();
   if(r?.status()!==200||found<1)fail("teaser-"+language+route,"Hub/home card missing");
  if(route==="/notes/"){
    const navItems=await tab.locator(".notes-hub-index li a").count();
    if(navItems!==5)fail("teaser-"+language,"Notes topic index must list all five items: "+navItems);
    if(await tab.locator('.notes-hub-index a[href="#conflict-article"]').count()!==1)fail("teaser-"+language,"Conflict article missing from Notes index");
  }
  }
  const published=await tab.goto(BASE+prefix+"/notes/first-consultation/",{waitUntil:"domcontentloaded",timeout:45000});
  if(published?.status()!==200||!await tab.locator("h1").count())fail("regression-"+language,"Existing article unavailable");
 }
 const response=await tab.goto(BASE+"/sitemap.xml",{waitUntil:"domcontentloaded",timeout:45000});
 const xml=await response.text();
 if(response.status()!==200||![canonical("uk"),canonical("ru")].every(x=>xml.includes("<loc>"+x+"</loc>")))fail("sitemap","Bilingual routes absent from sitemap");
 const uaSchemaCount=(xml.match(/<loc>/g)||[]).length;
 if(uaSchemaCount!==18)fail("sitemap","Expected 18 real indexable URLs, got "+uaSchemaCount);
 await tab.close();
}finally{await browser.close()}
await fs.writeFile(path.join(output,"report.json"),JSON.stringify({BASE,entries,errors},null,2));
await fs.writeFile(path.join(output,"report.txt"),["TASK 031 real Chromium bilingual QA",BASE,"16 viewport/language pairs",...errors.map(x=>"FAIL "+x),errors.length?"FAIL":"PASS"].join("\n"));
console.log("TASK031 bilingual Chrome QA: "+(errors.length?"FAIL "+errors.length:"PASS 16/16 viewport/language combos"));
for(const e of errors)console.error(e);
if(errors.length)process.exit(1);

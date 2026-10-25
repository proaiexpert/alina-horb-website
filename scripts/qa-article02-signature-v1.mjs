// TASK 046: cinematic editorial QA, 2 languages x 5 widths.
import { chromium } from "playwright";
import fs from "node:fs/promises";
import path from "node:path";

const base=(process.env.AUDIT_BASE_URL||"http://127.0.0.1:4177").replace(/\/$/,"");
const live=process.env.TASK046_LIVE==="1";
const output=process.env.TASK046_OUTPUT_DIR||"qa/task046-signature";
const expected=process.env.TASK046_EXPECTED_SHA||"";
const specs=[{lang:"ua",route:"/notes/fear-of-another-panic-attack/"},{lang:"ru",route:"/ru/notes/fear-of-another-panic-attack/"}];
// TASK 046B: test both sides of the content-driven 1120px layout switch.
const viewports=[{w:390,h:844},{w:430,h:932},{w:768,h:1024},
  {w:800,h:1000},{w:820,h:1000},{w:880,h:1000},{w:900,h:1000},
  {w:1024,h:768},{w:1119,h:900},{w:1120,h:900},{w:1440,h:1000}];
const results=[],failures=[];
const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
function verify(ok,message){if(!ok)throw Error(message);}

if(live){
 verify(base.startsWith("https://"),"Expected HTTPS Cloudflare host");
 verify(/^[0-9a-f]{40}$/.test(expected),"Expected full source SHA");
 let manifest,issue="";
 for(let i=0;i<32;i++){
  try{
   const r=await fetch(base+"/preview-build-info.json",{cache:"no-store",signal:AbortSignal.timeout(8000)});
   if(r.ok){manifest=await r.json();if(manifest.commit_sha===expected)break;issue="old commit "+manifest.commit_sha;}
   else issue="status "+r.status;
  }catch(e){issue=String(e);}
  await pause(8000);
 }
 verify(manifest?.commit_sha===expected,"Cloudflare has not deployed commit: "+issue);
 for(const u of ["/","/assets/images/notes/alina-horb-article02-hero-4x3.webp","/assets/images/notes/alina-horb-article02-home-card-800x500.webp","/assets/images/notes/alina-horb-article02-notes-card-800x600.webp","/assets/images/social/alina-horb-article02-og.png","/assets/css/site.article.panic.v1.css","/assets/js/site.navigation.v1.js","/assets/js/site.article.reading.v2.js",...specs.map(x=>x.route)]){
  const r=await fetch(base+u,{signal:AbortSignal.timeout(15000)});
  verify(r.status===200,"Cloudflare HTTP "+r.status+": "+u);
  verify(/\bnoindex\b/i.test(r.headers.get("x-robots-tag")||""),"Missing X-Robots-Tag on "+u);
 }
}
await fs.mkdir(output,{recursive:true});
const browser=await chromium.launch({headless:true});
try{
 for(const spec of specs)for(const vp of viewports){
  const page=await browser.newPage({viewport:{width:vp.w,height:vp.h},deviceScaleFactor:1,reducedMotion:"reduce"});
  await page.addInitScript(()=>{
    window.task046CLS=0;window.task046LCP=0;
    try{
      new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.task046CLS+=e.value;}).observe({type:"layout-shift",buffered:true});
      new PerformanceObserver(l=>{for(const e of l.getEntries())window.task046LCP=e.startTime;}).observe({type:"largest-contentful-paint",buffered:true});
    }catch(_){}
  });
  try{
   const r=await page.goto(base+spec.route,{waitUntil:"networkidle",timeout:30000});
   verify(r?.status()===200,"page HTTP 200");
   await page.evaluate(()=>document.fonts?.ready);
   const d=await page.evaluate(()=>{
    const sel=x=>document.querySelector(x);
    const box=e=>{if(!e)return null;let r=e.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height,bottom:r.bottom};};
    let hero=sel(".article-hero-visual img");
    let stages=[...document.querySelectorAll(".panic-steps li[data-step]")];
    const styleSize=s=>{const e=sel(s);return e?parseFloat(getComputedStyle(e).fontSize):null;};
    const clipped=e=>!!e&&e.scrollWidth>e.clientWidth+2;
    const typographicOverflow=[
      ".article-hero--v32 h1",".article-hero--v32 .article-meta",
      ".article-date-line",".article-hero-label",
      ".panic-map-heading h3",...stages.map((_,i)=>".panic-steps li:nth-child("+(i+1)+") strong")
    ].filter(s=>clipped(sel(s)));
    const visualLabels={captionPx:styleSize(".article-hero-label"),
      metaPx:styleSize(".article-hero--v32 .article-meta"),
      breadcrumbPx:styleSize(".article-breadcrumbs"),
      datePx:styleSize(".article-hero--v32 .article-date-line"),
      mapDescPx:styleSize(".panic-steps li p"),
      mapTitlePx:styleSize(".panic-steps li strong"),
      mapIndexPx:styleSize(".panic-map-index"),
      tocCountPx:styleSize(".panic-toc-count")};

    return {
     overflow:Math.max(0,document.documentElement.scrollWidth-innerWidth),
     heroLoaded:!!hero?.complete&&hero.naturalWidth===1200&&hero.naturalHeight===900,
     hero:box(hero),caption:box(sel(".article-hero-label")),h1:box(sel(".article-hero--v32 h1")),
     picture:box(sel(".article-hero-visual picture")),
     topArch:sel(".article-hero-visual picture")?getComputedStyle(sel(".article-hero-visual picture")).borderTopLeftRadius:"",
     bottomCorner:sel(".article-hero-visual picture")?getComputedStyle(sel(".article-hero-visual picture")).borderBottomLeftRadius:"",
     overlayAfter:getComputedStyle(sel(".article-hero-visual"),"::after").content,
     captionBackground:getComputedStyle(sel(".article-hero-label")).backgroundColor,
     tocRegion:box(sel(".article-toc")),
     imageFit:hero?getComputedStyle(hero).objectFit:null,
     railHidden:!sel(".article-hero-grid > .editorial-rail")||getComputedStyle(sel(".article-hero-grid > .editorial-rail")).display==="none",
     stages:stages.map(e=>e.dataset.step),stageRects:stages.map(box),
     mapMode:getComputedStyle(sel(".panic-steps ol")).display,
     mapColumns:getComputedStyle(sel(".panic-steps ol")).gridTemplateColumns,
     visualLabels,typographicOverflow,
     mapTitle:!!sel(".panic-map-heading h3"),noninevitable:!!sel(".panic-noninevitable"),
     faq:document.querySelectorAll("details.article-qa").length,
     toc:document.querySelectorAll(".article-toc > ol > li").length,
     cta:!!sel(".article-cta-band--v21 .article-cta-primary"),
     noindex:!!sel('meta[name="robots"]')?.content.includes("noindex"),
     CLS:Number(window.task046CLS||0),LCPms:Number(window.task046LCP||0)
    };
   });
   verify(d.overflow<=1,"horizontal overflow "+d.overflow);
   verify(d.heroLoaded&&d.hero?.w>250&&d.hero?.h>180,"Hero unloaded or cropped to invisible");
   verify(d.caption&&d.caption.y>=d.hero.bottom-2,"photo caption overlaps Hero");
   verify(d.picture?.w>250&&Math.abs(d.picture.w/d.picture.h-4/3)<.035,"arch loses 4:3 composition");
   verify(d.topArch?.includes("%")&&parseFloat(d.topArch)>=40,"arch silhouette missing");
   verify(parseFloat(d.bottomCorner)<=5,"arch lower corners no longer restrained");
   verify(d.overlayAfter==="none","Notes global ::after overlay tints figure or caption");
   verify(["transparent","rgba(0, 0, 0, 0)"].includes(d.captionBackground),"caption has unintended gray panel");
   if(vp.w<=430)verify(d.tocRegion?.y-d.caption.bottom<150,"mobile caption-to-TOC gap excessive");
   verify(d.h1?.w>Math.min(320,vp.w*.36)&&d.h1?.h>40&&d.h1?.h<900,"Hero headline collapsed into a narrow/vertical column");
   verify(d.imageFit==="cover","Hero image object fit invalid");
   verify(d.visualLabels.captionPx>=13 && d.visualLabels.captionPx<=14.5,
     "caption too small or oversized: "+d.visualLabels.captionPx);
   verify(d.visualLabels.metaPx>=12 && d.visualLabels.breadcrumbPx>=12 &&
     d.visualLabels.datePx>=12,"Hero microtype undersized: "+JSON.stringify(d.visualLabels));
   verify(d.visualLabels.mapDescPx>=16 && d.visualLabels.mapTitlePx>=25,
     "Step descriptions/title undersized: "+JSON.stringify(d.visualLabels));
   verify(d.visualLabels.mapIndexPx>=13,"Map index font undersized");
   verify(d.typographicOverflow.length===0,"Microtype or heading clipping: "+d.typographicOverflow.join(", "));
   verify(d.railHidden,"Desktop hydrated editorial rail overlays Hero composition");
   if(vp.w>=1120){
    verify(d.hero.w<vp.w*.65&&d.hero.x>d.h1.x+d.h1.w*.6,"Desktop columns or portrait composition broken");
   }
   verify(JSON.stringify(d.stages)===JSON.stringify(["01","02","03","04","05"]),"five-step order changed");
   verify(d.mapTitle&&d.noninevitable&&d.faq===6&&d.cta&&d.toc===10,"editorial module/FAQ/CTA missing");
   verify(d.noindex,"staged page without noindex");
   verify(d.stageRects.every(x=>x.w>165&&x.h>40),"map stage too narrow");
   if(vp.w>=1120) {
     verify(d.mapMode==="grid","wide desktop map not two-track");
     const [a,b]=d.stageRects;
     verify(b.x>a.x+80,"chess layout missing left/right alternation");
   } else {
     verify(d.mapMode==="block","map must linearize below 1120px");
     verify(d.stageRects.every(x=>Math.abs(x.x-d.stageRects[0].x)<2),
       "map step tracks are not aligned to a single column");
   }
   verify(d.stageRects.every((x,i)=>i===0||x.y>=d.stageRects[i-1].y+d.stageRects[i-1].h-1),
     "map stage vertical ordering/collision broken");
   if(vp.w<=768){
     const menu=page.locator("[data-menu-toggle]").first();
     if(await menu.isVisible()){
       await menu.click({timeout:12000});
       verify(await menu.getAttribute("aria-expanded")==="true","Mobile menu does not open");
       await menu.click({timeout:12000});
       verify(await menu.getAttribute("aria-expanded")==="false","Mobile menu does not close");
     }
   }
   if([390,768,900,1024,1120,1440].includes(vp.w)){
    await page.locator(".article-hero--v32").screenshot({path:path.join(output,spec.lang+"-"+vp.w+"-hero.png"),timeout:20000});
    // For a clean diagnostic crop only, remove sticky global chrome and focused skip link.
    // Functional header/focus tests run in independent GitHub audits.
    await page.addStyleTag({content:".site-header--canonical, .skip-link, a[href='#main-content']:focus {visibility:hidden!important}"});
    await page.locator(".panic-steps").screenshot({path:path.join(output,spec.lang+"-"+vp.w+"-map.png"),timeout:20000});
   }
   const faq=page.locator("details.article-qa").first();
   await faq.locator("summary").click({timeout:12000});
   verify(await faq.evaluate(e=>e.open),"FAQ toggle");
   if(vp.w<=900){const toc=page.locator(".panic-toc-mobile");await toc.locator("summary").click({timeout:12000});verify(await toc.evaluate(e=>e.open),"mobile TOC");}
   results.push({lang:spec.lang,width:vp.w,status:"PASS",...d});
  }catch(e){failures.push({lang:spec.lang,width:vp.w,error:String(e.stack||e)});}
  finally{await page.close();}
 }
}finally{await browser.close();}
await fs.writeFile(path.join(output,"report.json"),JSON.stringify({mode:live?"cloudflare-live":"local-stage",base,expectedSHA:expected,status:failures.length?"FAIL":"PASS",results,failures},null,2)+"\n");
console.log("TASK 046B signature typography/map:",results.length+"/"+(specs.length*viewports.length)+" PASS; failures="+failures.length+"; "+(live?"Cloudflare LIVE":"staged local"));
for(const f of failures)console.error(JSON.stringify(f));
if(failures.length)process.exitCode=1;

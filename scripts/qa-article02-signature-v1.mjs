// TASK 046: cinematic editorial QA, 2 languages x 5 widths.
import { chromium } from "playwright";
import fs from "node:fs/promises";
import path from "node:path";

const base=(process.env.AUDIT_BASE_URL||"http://127.0.0.1:4177").replace(/\/$/,"");
const live=process.env.TASK046_LIVE==="1";
const output=process.env.TASK046_OUTPUT_DIR||"qa/task046-signature";
const expected=process.env.TASK046_EXPECTED_SHA||"";
const specs=[{lang:"ua",route:"/notes/fear-of-another-panic-attack/"},{lang:"ru",route:"/ru/notes/fear-of-another-panic-attack/"}];
const viewports=[{w:390,h:844},{w:430,h:932},{w:768,h:1024},{w:1024,h:768},{w:1440,h:1000}];
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
 for(const u of ["/","/assets/images/notes/alina-horb-article02-hero-4x3.webp","/assets/images/notes/alina-horb-article02-home-card-800x500.webp","/assets/images/notes/alina-horb-article02-notes-card-800x600.webp","/assets/images/social/alina-horb-article02-og.png",...specs.map(x=>x.route)]){
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
    return {
     overflow:Math.max(0,document.documentElement.scrollWidth-innerWidth),
     heroLoaded:!!hero?.complete&&hero.naturalWidth===1200&&hero.naturalHeight===900,
     hero:box(hero),caption:box(sel(".article-hero-label")),h1:box(sel(".article-hero--v32 h1")),
     imageFit:hero?getComputedStyle(hero).objectFit:null,
     stages:stages.map(e=>e.dataset.step),stageRects:stages.map(box),
     mapMode:getComputedStyle(sel(".panic-steps ol")).display,
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
   verify(d.h1?.w>Math.min(320,vp.w*.36)&&d.h1?.h>40&&d.h1?.h<900,"Hero headline collapsed into a narrow/vertical column");
   verify(d.imageFit==="cover","Hero image object fit invalid");
   if(vp.w>=1120){
    verify(d.hero.w<vp.w*.65&&d.hero.x>d.h1.x+d.h1.w*.6,"Desktop columns or portrait composition broken");
   }
   verify(JSON.stringify(d.stages)===JSON.stringify(["01","02","03","04","05"]),"five-step order changed");
   verify(d.mapTitle&&d.noninevitable&&d.faq===6&&d.cta&&d.toc===10,"editorial module/FAQ/CTA missing");
   verify(d.noindex,"staged page without noindex");
   verify(d.stageRects.every(x=>x.w>165&&x.h>40),"map stage too narrow");
   if(vp.w>=1024)verify(d.mapMode==="grid","desktop map not two-track");
   if(vp.w<=768)verify(d.mapMode==="block","small viewport map not linear");
   if([390,768,1440].includes(vp.w)){
    await page.locator(".article-hero--v32").screenshot({path:path.join(output,spec.lang+"-"+vp.w+"-hero.png"),timeout:20000});
    await page.locator(".panic-steps").screenshot({path:path.join(output,spec.lang+"-"+vp.w+"-map.png"),timeout:20000});
   }
   const faq=page.locator("details.article-qa").first();
   await faq.locator("summary").click({timeout:12000});
   verify(await faq.evaluate(e=>e.open),"FAQ toggle");
   if(vp.w<=768){const toc=page.locator(".panic-toc-mobile");await toc.locator("summary").click({timeout:12000});verify(await toc.evaluate(e=>e.open),"mobile TOC");}
   results.push({lang:spec.lang,width:vp.w,status:"PASS",...d});
  }catch(e){failures.push({lang:spec.lang,width:vp.w,error:String(e.stack||e)});}
  finally{await page.close();}
 }
}finally{await browser.close();}
await fs.writeFile(path.join(output,"report.json"),JSON.stringify({mode:live?"cloudflare-live":"local-stage",base,expectedSHA:expected,status:failures.length?"FAIL":"PASS",results,failures},null,2)+"\n");
console.log("TASK 046 signature:",results.length+"/10 PASS; failures="+failures.length+"; "+(live?"Cloudflare LIVE":"staged local"));
for(const f of failures)console.error(JSON.stringify(f));
if(failures.length)process.exitCode=1;

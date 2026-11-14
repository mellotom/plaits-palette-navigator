(function(){
var D=window.__PP;if(!D)return;
var BANKS=[['green','#4F9B6A','tonal voices'],['red','#C9534F','noise · physical · drums'],['amber','#D69B35','digital · alternate'],['orange','#DD6E37','fourth bank']];
var LED=[['green','#4F9B6A',0],['red','#C9534F',0],['yellow','#D6B635',0],['green','#4F9B6A',1],['red','#C9534F',1],['yellow','#D6B635',1]];
var KEY='pp-guide',FKEY='pp-file';
var G=null,ORIG=null;
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function $(id){return document.getElementById(id);}
function pad2(n){return (n<10?'0':'')+n;}
function B(x){return '<span class="b">[ '+x+' ]</span>';}

// ---------- reading a configuration ----------
function parse(text){
  var o;try{o=JSON.parse(text);}catch(e){throw new Error('that file isn’t readable as a palette configuration');}
  var r=(o&&o.recipe&&typeof o.recipe==='object')?o.recipe:o;
  if(!r||!Array.isArray(r.slots)||(r.slots.length!==24&&r.slots.length!==32))throw new Error('no 24 or 32 slot palette found in that file');
  var g={name:(typeof o.name==='string'&&o.name)?o.name.slice(0,60):'',slots:[],nav:'',opt:{},pref:{},ct:[],fm:{},extra:[],target:typeof r.target==='string'?r.target:''};
  r.slots.forEach(function(s){var id=(s&&typeof s==='object')?s.engine:s;if(typeof id!=='string'||!id){g.slots.push(null);return;}if(D.retired[id])id=D.retired[id];g.slots.push(id);});
  var p=r.preferences||{},q=r.initialOptions||{};
  if(p.navigationMode==='linear'||p.navigationMode==='banked')g.nav=p.navigationMode;
  ['syncInput','envelopeContour','calibration','colorBlindMode','replaceableFmBanks','linearTzfm','fastFm','simplifiedPitchRanges','quickRetune'].forEach(function(k){if(p[k]===true)g.pref[k]=1;});
  ['auxOutput','suboscillatorOctave','lockedFrequencyKnob','trigResponse','modelInput','levelInput','holdOnTrigger','attenuverterMode','chordTable'].forEach(function(k){if(q[k]!==undefined&&(typeof q[k]==='string'||typeof q[k]==='number'||typeof q[k]==='boolean'))g.opt[k]=q[k];});
  var res=r.resources||{};
  if(Array.isArray(res.chordTables))res.chordTables.forEach(function(t){if(!t||typeof t!=='object')return;g.ct.push({id:String(t.id||''),n:String(t.name||t.id||'').slice(0,40),a:String(t.author||'').slice(0,40),c:(Array.isArray(t.chords)?t.chords:[]).map(function(c){return String((c&&c.name)||'').slice(0,24);})});});
  if(Array.isArray(res.userDataBanks))res.userDataBanks.forEach(function(e){
    if(!e||typeof e.slot!=='number'||!e.bank||!Array.isArray(e.bank.voices))return;
    g.fm[e.slot]=e.bank.voices.map(function(v){var pk=v&&v.packed;if(!Array.isArray(pk)||pk.length<128)return '';var s='';for(var i=118;i<128;i++){var ch=pk[i];s+=(ch>=32&&ch<127)?String.fromCharCode(ch):' ';}return s.replace(/\s+$/,'');});});
  [['customModelData','custom wavetable / terrain data'],['wavetableBank','a custom wavetable bank'],['terrainBank','a custom terrain bank'],['speechBanks','custom speech banks'],['naturalSpeechBanks','natural speech word banks'],['scaleBank','a custom scale bank']].forEach(function(x){var v=res[x[0]];if(v&&((Array.isArray(v)&&v.length)||(!Array.isArray(v)&&typeof v==='object'&&Object.keys(v).length)))g.extra.push(x[1]);});
  return g;
}
// ---------- share link (deflate + base64url) ----------
function b64(u8){var s='';for(var i=0;i<u8.length;i++)s+=String.fromCharCode(u8[i]);return btoa(s).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');}
function unb64(t){t=t.replace(/-/g,'+').replace(/_/g,'/');while(t.length%4)t+='=';var s=atob(t),u=new Uint8Array(s.length);for(var i=0;i<s.length;i++)u[i]=s.charCodeAt(i);return u;}
function pipe(u8,T,arg){return new Response(new Blob([u8]).stream().pipeThrough(new T(arg))).arrayBuffer().then(function(b){return new Uint8Array(b);});}
function pack(g){var u=new TextEncoder().encode(JSON.stringify(g));if(window.CompressionStream)return pipe(u,CompressionStream,'deflate-raw').then(function(z){return 'z'+b64(z);}).catch(function(){return 'j'+b64(u);});return Promise.resolve('j'+b64(u));}
function unpack(t){var k=t.charAt(0),u=unb64(t.slice(1));var d=new TextDecoder();if(k==='j')return Promise.resolve(JSON.parse(d.decode(u)));if(k==='z'&&window.DecompressionStream)return pipe(u,DecompressionStream,'deflate-raw').then(function(x){return JSON.parse(d.decode(x));});return Promise.reject(new Error('this browser can’t open that share link'));}
function clean(g){ // a guide from a link or storage goes through the same checks as a file
  if(!g||!Array.isArray(g.slots)||(g.slots.length!==24&&g.slots.length!==32))throw new Error('bad link');
  return parse(JSON.stringify({name:g.name,recipe:{slots:g.slots,target:g.target,preferences:Object.assign({navigationMode:g.nav},Object.keys(g.pref||{}).reduce(function(a,k){a[k]=true;return a;},{})),initialOptions:g.opt||{},resources:{chordTables:(g.ct||[]).map(function(t){return{id:t.id,name:t.n,author:t.a,chords:(t.c||[]).map(function(n){return{name:n};})};})}}}),g.fm,g.extra);
}
function adopt(g,src){var c=clean(g);c.fm={};Object.keys(src.fm||{}).forEach(function(k){if(Array.isArray(src.fm[k]))c.fm[k]=src.fm[k].map(function(n){return String(n).slice(0,10);});});c.extra=(src.extra||[]).map(function(x){return String(x).slice(0,60);});return c;}

// ---------- rendering ----------
function model(id){return D.models[id]||null;}
function bankOf(i){return BANKS[Math.floor(i/8)];}
function leds(n,col){var h='<span class="leds" aria-hidden="true">';for(var j=0;j<8;j++)h+='<i'+(j===n?' style="background:'+col+'"':'')+'></i>';return h+'</span>';}
function fmNames(i,id){if(G.fm[i])return G.fm[i];var k={'dx7-bank-a':0,'dx7-bank-b':1,'dx7-bank-c':2}[id];return k===undefined?null:D.dx7[k];}
function status(msg,bad){var e=$('pp-status');if(!e)return;e.textContent=msg;e.className='pp-status'+(bad?' bad':'');}
function optIndex(){var o=G.opt,ix={};
  ix[0]=o.auxOutput===undefined?null:({'alternate-model':0,'stereo':1,'square-subosc':2,'sine-subosc':2})[o.auxOutput];
  ix[1]=(o.suboscillatorOctave===undefined)?null:((o.auxOutput==='sine-subosc'?3:0)+({'0':0,'-1':1,'-2':2})[String(o.suboscillatorOctave)]);
  ix[2]=o.lockedFrequencyKnob===undefined?null:({'octaves':0,'macro-4':1,'aux-crossfade':2,'decay':3,'triggered-envelope':4,'gated-envelope':4,'envelope-contour':4})[o.lockedFrequencyKnob];
  var tr=o.trigResponse!==undefined?o.trigResponse:(o.lockedFrequencyKnob==='gated-envelope'?'gate':'trigger');
  ix[3]=({'trigger':0,'gate':1,'velocity-trigger':2,'velocity-gate':3})[tr];
  ix[4]=o.modelInput===undefined?null:({'model':0,'macro-4':1,'aux-crossfade':2,'lpg-colour':3,'sync-in':4})[o.modelInput];
  ix[5]=o.levelInput===undefined?null:({'level':0,'decay':1,'auto':2})[o.levelInput];
  ix[6]=o.holdOnTrigger===undefined?null:(o.holdOnTrigger?1:0);
  ix[7]=({'stock':0,'drift':1,'step':2})[o.attenuverterMode===undefined?'stock':o.attenuverterMode];
  return ix;}
function lights(){
  var contour=G.pref.envelopeContour||/envelope/.test(String(G.opt.lockedFrequencyKnob||''));
  var L=[['aux output',['regular aux model','stereo (out / aux = l / r)','suboscillator']],
   ['suboscillator',['square','square, −1 octave','square, −2 octaves','sine','sine, −1 octave','sine, −2 octaves']],
   ['frequency knob',['octaves','twist (fourth control)','aux crossfade','lpg decay'].concat(contour?['envelope contour']:[])],
   ['trig response',['trigger','gate','velocity trigger','velocity gate'],[0,1,3,4]],
   ['model input',['model select','twist (fourth control)','aux crossfade','lpg colour (vcfa › vca)'].concat(G.pref.syncInput?['sync in (experimental)']:[])],
   ['level input',['level','lpg decay','auto: decay or velocity']],
   ['hold on trigger',['off (live cv)','sample + hold']],
   ['unpatched attenuverters',['default behaviour','continuous drift','triggered random step']]];
  var ix=optIndex(),h='';
  L.forEach(function(l,i){
    h+='<div class="r lt"><div class="kc"><span class="v">light '+(i+1)+'</span><br><span class="b">'+l[0]+'</span></div><div class="a">';
    l[1].forEach(function(m,j){var st=LED[l[2]?l[2][j]:j],on=ix[i]===j;
      h+='<span class="ov'+(on?' on':'')+'"><i class="dot'+(st[2]?' bl':'')+'" style="background:'+st[1]+'"></i>'+esc(m)+(on?' <em>◂ starts here</em>':'')+'</span>';});
    h+='</div></div>';});
  return h;}
function render(){
  var has=!!G,slots=has?G.slots:[],nb=slots.length/8,used=slots.filter(function(x){return x;});
  document.documentElement.classList.toggle('pp-has',has);
  $('pp-share').hidden=!has;$('pp-clear').hidden=!has;$('pp-dl').hidden=!(has&&ORIG);
  // voice index
  var h='';
  if(!has){h='<p class="pp-wait">load a configuration and the four banks appear here: every slot, in LED order.</p>';}
  else for(var b=0;b<nb;b++){var bk=BANKS[b];
    h+='<div class="bk"><div class="bkh"><span class="sn" style="background:'+bk[1]+';color:#1F1B19">'+(b+1)+'</span><span class="bkn">'+bk[0]+'</span><span class="sc">'+bk[2]+'</span></div>';
    for(var j=0;j<8;j++){var i=b*8+j,id=slots[i],m=id&&model(id);
      h+='<div class="ix"><span class="ixn">'+pad2(j+1)+'</span>'+leds(j,bk[1])+(id?('<span class="ixt">'+esc(m?m.n:id)+'</span><span class="ixf">'+(m?esc(m.f.toLowerCase()):'not in this catalog')+'</span>'):'<span class="ixt z">empty slot</span>')+'</div>';}
    h+='</div>';}
  $('pp-index').innerHTML=h;
  // options
  $('pp-opts').innerHTML=has?lights():'<p class="pp-wait">the eight menu lights and where this build starts each one.</p>';
  var notes=[];
  if(has){
    notes.push('model navigation: <b>'+(G.nav||'not stated in the file')+'</b>'+(G.nav==='linear'?' · the buttons step through every model and roll into the next bank':''));
    var pf=[];if(G.pref.calibration)pf.push('calibration procedure');if(G.pref.colorBlindMode)pf.push('colour-blind bank display (brightness, not hue)');if(G.pref.replaceableFmBanks)pf.push('fm banks replaceable by audio into timbre');if(G.pref.syncInput)pf.push('sync in');if(G.pref.envelopeContour)pf.push('frequency envelope contour');if(G.pref.linearTzfm)pf.push('linear tzfm');if(G.pref.fastFm)pf.push('50 khz fast fm (level cv unavailable)');if(G.pref.simplifiedPitchRanges)pf.push('simplified frequency ranges');if(G.pref.quickRetune)pf.push('quick retune');
    if(pf.length)notes.push('built in: '+pf.map(esc).join(' · '));
    if(G.extra.length)notes.push('also in this build, not listed here: '+G.extra.map(esc).join(' · '));
    if(G.target&&G.target!=='mutable-instruments-plaits')notes.push('target: <b>'+esc(G.target)+'</b> · button moves on this page are for the two-button plaits panel');
  }
  $('pp-notes').innerHTML=notes.map(function(n){return '<p class="note">'+n+'</p>';}).join('');
  // model sheets
  document.querySelectorAll('.pp-dyn').forEach(function(e){e.remove();});
  if(has){
    var tail=$('pp-tail'),ns=Math.ceil(nb/2);
    for(var s=0;s<ns;s++){
      var w=document.createElement('div');w.innerHTML=D.sheetHtml.replace(/__N__/g,String(s+2));var fr=w.firstElementChild;fr.classList.add('pp-dyn');
      tail.parentNode.insertBefore(fr,tail);
      var cols=fr.querySelectorAll('.col.pm');
      for(var k=0;k<2;k++){var b2=s*2+k;if(b2>=nb)continue;var bk2=BANKS[b2];
        for(var half=0;half<2;half++){var html=half===0?('<div class="sh"><span class="sn" style="background:'+bk2[1]+';color:#1F1B19">'+(b2+1)+'</span><h2 class="st">'+bk2[0]+' bank · 1–4</h2><span class="sc">'+bk2[2]+'</span></div>'):('<div class="sh"><span class="sn" style="background:'+bk2[1]+';color:#1F1B19">'+(b2+1)+'</span><h2 class="st">'+bk2[0]+' bank · 5–8</h2><span class="sc">continued</span></div>');
          for(var j2=half*4;j2<half*4+4;j2++)html+=card(b2*8+j2,j2,bk2);
          cols[k*2+half].innerHTML='<div class="zc"><section class="sec">'+html+'</section></div>';}}
      fr.querySelector('.col.px').innerHTML='<div class="zc">'+(s===0?chordsHtml()+twistHtml():fmHtml(true))+'</div>';
      if(ns===1)fr.querySelector('.col.px').innerHTML='<div class="zc">'+chordsHtml()+fmHtml(false)+twistHtml()+'</div>';
    }
  }
  // header stats on every sheet
  var uniq={};used.forEach(function(x){uniq[x]=1;});
  document.querySelectorAll('.pp-st-models').forEach(function(e){e.textContent=has?used.length:'—';});
  document.querySelectorAll('.pp-st-banks').forEach(function(e){e.textContent=has?nb:'—';});
  document.querySelectorAll('.pp-st-tables').forEach(function(e){e.textContent=has?G.ct.length:'—';});
  document.querySelectorAll('.pp-name').forEach(function(e){e.textContent=has?(G.name||'untitled palette'):'no palette loaded';});
  document.title=has?('plaits palette · '+(G.name||'custom guide')):D.title;
  syncTm();window.dispatchEvent(new Event('resize'));
  setTimeout(fitAll,30);setTimeout(fitAll,400);
}
function card(i,j,bk){var id=G.slots[i];
  if(!id)return '<div class="md"><div class="mh"><span class="mn" style="background:'+bk[1]+';color:#1F1B19">'+(j+1)+'</span><span class="mt z">empty slot</span>'+leds(j,bk[1])+'</div></div>';
  var m=model(id);
  if(!m)return '<div class="md"><div class="mh"><span class="mn" style="background:'+bk[1]+';color:#1F1B19">'+(j+1)+'</span><span class="mt">'+esc(id)+'</span>'+leds(j,bk[1])+'</div><div class="mdd">this model isn’t in the catalog this page was built from ('+esc(D.pulled)+'), so there is nothing certain to show for it.</div></div>';
  var rows=[['harmonics',m.c[0],m.h],['timbre',m.c[1],m.t],['morph',m.c[2],m.m],['twist',m.c[3],m.w]].map(function(r){return '<div class="mr"><span class="mk">'+r[0]+'</span><span class="ma"><b>'+esc(r[1])+'</b> · '+esc(r[2])+'</span></div>';}).join('');
  rows+='<div class="mr io"><span class="mk">out</span><span class="ma">'+esc(m.out)+'</span></div><div class="mr io"><span class="mk">aux</span><span class="ma">'+esc(m.aux)+'</span></div><div class="mr io"><span class="mk">trig</span><span class="ma">'+esc(m.trig)+'</span></div>';
  return '<div class="md"><div class="mh"><span class="mn" style="background:'+bk[1]+';color:#1F1B19">'+(j+1)+'</span><span class="mt">'+esc(m.n)+'</span><span class="mdsc">'+esc(m.f.toLowerCase())+' · '+esc(m.a.toLowerCase())+'</span>'+leds(j,bk[1])+'</div><div class="mdd">'+esc(m.d)+'</div>'+rows+'</div>';}
function chordsHtml(){
  var ids={chords:1,'string-machine':1,chiptune:1},uses=G.slots.filter(function(x){return x&&(ids[x]||/chord/.test(x));});
  if(!G.ct.length)return '';
  var h='<section class="sec"><div class="sh"><span class="sn" style="background:#D6B635;color:#1F1B19">ct</span><h2 class="st">chord tables</h2><span class="sc">'+G.ct.length+' loaded</span></div>';
  h+='<div class="r"><div class="kc">'+B('left')+' <span class="v">hold</span><i class="p">+</i><span class="v">turn</span> '+B('harmonics')+'</div><div class="a">pick a table while a chord model is active. tables 1–8 show one yellow light; 9–16 show seven yellow lights with the chosen position dark</div></div>';
  G.ct.forEach(function(t,i){h+='<div class="ctb"><div class="cth"><span class="ixn">'+pad2(i+1)+'</span><span class="ctn">'+esc(t.n)+'</span><span class="mdsc">'+(t.a?esc(t.a.toLowerCase())+' · ':'')+t.c.length+' positions'+(G.opt.chordTable===t.id?' · <b>starts here</b>':'')+'</span></div><div class="ctc">'+t.c.map(function(c,k){return '<span><i>'+(k+1)+'</i>'+esc(c)+'</span>';}).join('')+'</div></div>';});
  return h+'</section>';}
function fmHtml(first){
  var h='',n=0;
  G.slots.forEach(function(id,i){if(!id)return;var nm=fmNames(i,id);if(!nm)return;var bk=bankOf(i),m=model(id);n++;
    h+='<div class="ctb"><div class="cth"><span class="mn" style="background:'+bk[1]+';color:#1F1B19">'+((i%8)+1)+'</span><span class="ctn">'+esc(m?m.n:id)+'</span><span class="mdsc">'+bk[0]+' '+((i%8)+1)+' · '+nm.length+' patches'+(G.fm[i]?' · custom bank':'')+'</span></div><div class="ctc fm">'+nm.map(function(c,k){return '<span><i>'+(k+1)+'</i>'+esc(c||'—')+'</span>';}).join('')+'</div></div>';});
  if(!n)return first?'':'';
  return '<section class="sec"><div class="sh"><span class="sn" style="background:#D69B35;color:#1F1B19">fm</span><h2 class="st">6-op fm patches</h2><span class="sc">harmonics picks the patch</span></div>'+h+'</section>';}
function twistHtml(){
  return '<section class="sec"><div class="sh"><span class="sn" style="background:#4F9B6A;color:#1F1B19">tw</span><h2 class="st">twist + fine tuning</h2><span class="sc">two-button panel</span></div>'+
  '<div class="r"><div class="kc"><span class="b h">[ right ]</span><i class="p">+</i><span class="v">turn</span> '+B('harmonics')+'</div><div class="a">until the model LEDs blink yellow: the octave-switching frequency range</div></div>'+
  '<div class="r"><div class="kc">'+B('left')+'<i class="p">+</i>'+B('right')+' <span class="v">tap</span></div><div class="a">options menu. '+B('left')+' walks to <b>light 3</b>, '+B('right')+' once until it turns red, both again to exit</div></div>'+
  '<div class="r"><div class="kc">'+B('frequency')+'</div><div class="a">now plays each model’s <b>twist</b>, its fourth control. on mutable instruments models, noon keeps the original sound</div></div>'+
  '<div class="r"><div class="kc"><span class="v">fine tuning</span></div><div class="a">the range position after octave switching, before the high-frequency range: all eight lights pulse together. release, then '+B('frequency')+' tunes ± one semitone. it saves two seconds after you stop and survives power cycles</div></div></section>';}

// ---------- fit the model sheets ----------
function sheetMode(){return !(window.__ew&&window.__ew()<900)&&!document.documentElement.classList.contains('tall');}
function fitAll(){
  document.querySelectorAll('.pp-dyn').forEach(function(fr){
    var zs=[].slice.call(fr.querySelectorAll('.zc'));zs.forEach(function(z){z.style.zoom='';});
    if(!sheetMode())return;
    var foot=fr.querySelector('footer');if(!foot)return;
    function over(z){var lim=foot.getBoundingClientRect().top;return zs.some(function(e){e.style.zoom=String(z);return e.getBoundingClientRect().bottom>lim-6*(lim/1366||1);});}
    function set(z){zs.forEach(function(e){e.style.zoom=String(z);});}
    set(1);if(!zs.some(function(e){return e.getBoundingClientRect().bottom>foot.getBoundingClientRect().top-4;}))return;
    var lo=.45,hi=1;for(var q=0;q<9;q++){var mid=(lo+hi)/2;set(mid);var bad=zs.some(function(e){return e.getBoundingClientRect().bottom>foot.getBoundingClientRect().top-4;});if(bad)hi=mid;else lo=mid;}
    set(lo);});
}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.pp-dyn .tm[data-t],.pp-dyn .tm[data-v]');if(!b)return;var k=b.hasAttribute('data-t')?'data-t':'data-v';var o=document.querySelector('#sheet .tm['+k+'="'+b.getAttribute(k)+'"]');if(o)o.click();setTimeout(syncTm,0);});
function syncTm(){document.querySelectorAll('.pp-dyn .tm[data-t]').forEach(function(b){var o=document.querySelector('#sheet .tm[data-t="'+b.getAttribute('data-t')+'"]');if(o)b.setAttribute('aria-pressed',o.getAttribute('aria-pressed'));});}
document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#sheet .tm[data-t]'))setTimeout(syncTm,0);});
var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(fitAll,120);});
window.addEventListener('beforeprint',fitAll);

// ---------- loading, saving ----------
function save(){try{if(G)localStorage.setItem(KEY,JSON.stringify(G));else{localStorage.removeItem(KEY);localStorage.removeItem(FKEY);}if(ORIG)localStorage.setItem(FKEY,JSON.stringify(ORIG));else localStorage.removeItem(FKEY);}catch(e){}}
function load(text,name){try{G=parse(text);ORIG={name:name||'my-plaits-palette.plaits-palette.json',text:text};save();render();status('loaded: '+(G.name||name||'palette')+' · remembered in this browser');try{history.replaceState(null,'',location.pathname+location.search);}catch(e){}}catch(e){status(e.message,true);}}
function readFile(f){if(!f)return;if(f.size>4e6){status('that file is too large to be a palette configuration',true);return;}var r=new FileReader();r.onload=function(){load(String(r.result),f.name);};r.onerror=function(){status('couldn’t read that file',true);};r.readAsText(f);}
$('pp-file').addEventListener('change',function(e){readFile(e.target.files[0]);e.target.value='';});
$('pp-pick').addEventListener('click',function(){$('pp-file').click();});
var dz=$('pp-drop');['dragenter','dragover'].forEach(function(n){dz.addEventListener(n,function(e){e.preventDefault();dz.classList.add('over');});});['dragleave','drop'].forEach(function(n){dz.addEventListener(n,function(e){e.preventDefault();dz.classList.remove('over');});});
dz.addEventListener('drop',function(e){var f=e.dataTransfer&&e.dataTransfer.files&&e.dataTransfer.files[0];readFile(f);});
$('pp-stock').addEventListener('click',function(){G=parse(JSON.stringify({name:'stock plaits',recipe:{slots:D.stock}}));ORIG=null;save();render();status('showing the stock 24-model lineup as an example');});
$('pp-clear').addEventListener('click',function(){G=null;ORIG=null;save();try{history.replaceState(null,'',location.pathname+location.search);}catch(e){}render();status('cleared');});
$('pp-dl').addEventListener('click',function(){if(!ORIG)return;var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([ORIG.text],{type:'application/json'}));a.download=ORIG.name;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},500);});
$('pp-share').addEventListener('click',function(){if(!G)return;pack(G).then(function(t){var u=location.origin+location.pathname+'#p='+t;try{history.replaceState(null,'','#p='+t);}catch(e){}
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(u).then(function(){status('share link copied · it opens this exact guide on any device');},function(){status('share link is in the address bar · copy it from there');});else status('share link is in the address bar · copy it from there');});});
function boot(){
  var m=/[#&]p=([A-Za-z0-9_-]+)/.exec(location.hash||'');
  if(m){unpack(m[1]).then(function(g){G=adopt(g,g);ORIG=null;save();render();status('opened from a share link · remembered in this browser');}).catch(function(){status('that share link couldn’t be read',true);stored();});return;}
  stored();}
function stored(){try{var t=localStorage.getItem(KEY);if(t){var g=JSON.parse(t);G=adopt(g,g);var f=localStorage.getItem(FKEY);ORIG=f?JSON.parse(f):null;}}catch(e){G=null;ORIG=null;}render();if(G)status('showing '+(G.name||'your palette')+' · remembered in this browser');}
boot();
})();

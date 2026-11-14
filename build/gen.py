# builds plaits-palette-navigator/index.html
# usage: python3 gen.py <plaits-navigator/index.html (style template)> <out index.html>
import json, os, re, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
tpl = open(sys.argv[1], encoding='utf-8').read()
out = sys.argv[2]
models = json.load(open(os.path.join(HERE, 'models.json'), encoding='utf-8'))
dx7 = json.load(open(os.path.join(HERE, 'dx7_stock.json'), encoding='utf-8'))
stock = json.load(open(os.path.join(HERE, 'stock.json'), encoding='utf-8'))
panel = open(os.path.join(HERE, 'panel.svg'), encoding='utf-8').read().replace('--pl', '--c')
PULLED = '2026.11.14'
REV = datetime.date.today().strftime('%Y.%m')
TITLE = 'plaits-palette-navigator · travelers guide for decoding the voice index'

INK = 'var(--c1F1B18)'; MUTE = 'var(--c7A7068)'; ACC = 'var(--cE2622B)'
U = 'color: inherit; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 2px'

# ---- head
head = tpl[:tpl.find('</head>')]
head = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', head, count=1)
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="plaits palette: load your rubato audio plaits palette configuration and get a guide to your own firmware. every model in every bank with what each knob does, the options menu, chord tables and fm patches.">', head, count=1)
CSS = '''
.frame{position:relative;overflow:hidden;background:var(--cF3EDE2);width:100vw;height:56.25vw}
.sheet{position:absolute;top:0;left:0;width:2560px;height:1440px;transform-origin:0 0;box-sizing:border-box;background:var(--cF3EDE2);color:var(--c1F1B18);display:flex;flex-direction:column;padding:0 64px}
.pp-wait{font-family:'Roboto Mono',monospace;font-size:11px;line-height:1.55;color:var(--c7A7068);margin:6px 0;max-width:420px}
.pp-status{font-family:'Roboto Mono',monospace;font-size:11px;line-height:1.5;color:var(--c1F1B18);margin:8px 0 0;min-height:17px}
.pp-status.bad{color:var(--cE2622B);font-weight:600}
.pp-drop{border:2px dashed var(--c1F1B18);padding:14px 14px 12px;margin:8px 0 0;display:flex;flex-direction:column;gap:8px;align-items:flex-start}
.pp-drop.over{background:var(--cEAE2D3)}
.pp-btn{font-family:'Roboto Mono',monospace;font-weight:600;font-size:11.5px;color:var(--c1F1B18);background:var(--cF3EDE2);border:1.5px solid var(--c1F1B18);padding:7px 10px;cursor:pointer;min-height:34px}
.pp-btn.go{background:var(--c1F1B18);color:var(--cF3EDE2)}
.pp-btn:hover{border-color:var(--cE2622B);color:var(--cE2622B)}.pp-btn.go:hover{background:var(--cE2622B);color:#fff}
.pp-btn[hidden]{display:none}
.pp-acts{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.bks{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px 28px}
.bkh{display:flex;align-items:stretch;border-top:4px solid var(--c1F1B18);margin-bottom:3px}
.bkn{font-family:'Archivo',sans-serif;font-weight:900;font-size:19px;line-height:1;letter-spacing:-.015em;padding:6px 10px 3px;flex:1}
.ix{display:grid;grid-template-columns:22px 50px minmax(0,1fr) auto;column-gap:10px;align-items:center;padding:6px 0;border-top:1px solid var(--cDDD3C3)}
.bkh + .ix{border-top:0}
.ixn{font-family:'Roboto Mono',monospace;font-weight:600;font-size:11px;color:var(--c7A7068)}
.ixt{font-family:'Archivo',sans-serif;font-weight:800;font-size:15px;letter-spacing:-.01em;color:var(--c1F1B18);min-width:0}
.ixt.z,.mt.z{color:var(--c7A7068);font-weight:500}
.ixf{font-family:'Roboto Mono',monospace;font-size:10px;color:var(--c7A7068);white-space:nowrap}
.leds{display:inline-flex;gap:2px;flex:none}.leds i{width:4px;height:9px;background:var(--cDDD3C3)}
.mh .leds{margin-left:8px}
.r.lt{grid-template-columns:132px minmax(0,1fr)}.r.lt .b{white-space:normal}.m-legend .r{grid-template-columns:86px minmax(0,1fr)}
.ov{display:inline-flex;align-items:center;gap:5px;margin:0 12px 1px 0;white-space:nowrap}
.ov.on{font-weight:700;color:var(--c1F1B18)}
.ov em{font-style:normal;font-family:'Roboto Mono',monospace;font-size:10px;font-weight:600;color:var(--cE2622B)}
.dot{width:8px;height:8px;border-radius:50%;flex:none;display:inline-block}
.dot.bl{box-shadow:0 0 0 2px var(--cF3EDE2),0 0 0 3px currentColor;margin:0 3px}
.mdd{font-family:'Archivo',sans-serif;font-size:12px;line-height:1.3;color:var(--c1F1B18);margin:1px 0 3px}
.mr.io .mk{color:var(--c1F1B18);font-weight:600}
.mr{grid-template-columns:66px minmax(0,1fr)!important}
.ma b{font-weight:700;color:var(--c1F1B18)}
.ctb{padding:6px 0 7px;border-top:1px solid var(--cDDD3C3)}
.cth{display:flex;align-items:baseline;gap:8px;margin-bottom:3px}
.ctn{font-family:'Archivo',sans-serif;font-weight:800;font-size:14px;color:var(--c1F1B18)}
.cth .mdsc b{color:var(--cE2622B)}
.ctc{display:flex;flex-wrap:wrap;gap:1px 10px;font-family:'Archivo',sans-serif;font-size:11.5px;line-height:1.35;color:var(--c4A433D)}
.ctc i{font-style:normal;font-family:'Roboto Mono',monospace;font-size:9.5px;color:var(--c7A7068);margin-right:3px}
.ctc.fm{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));font-family:'Roboto Mono',monospace;font-size:10px;gap:0 8px}
.ctc.fm span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.zc{display:flex;flex-direction:column;gap:14px;min-width:0}
.pp-fig{border:1px solid var(--c1F1B18);margin-top:2px}
@media print{.pp-drop,.pp-acts,.pp-status{display:none!important}:root:not([data-pdf]) .frame,:root:not([data-pdf]) .sheet{background:#FFFFFF!important}}
@media screen and (max-width: 899px){
.frame{width:auto!important;height:auto!important;overflow:visible!important}
.sheet{position:static!important;width:auto!important;height:auto!important;transform:none!important;padding:0 16px!important}
.frame + .frame{margin-top:40px}
.bks{grid-template-columns:minmax(0,1fr)!important}
.m-grid>.col{grid-column:auto!important}
.r.lt{grid-template-columns:minmax(0,34%) minmax(0,1fr)!important}
.ov{white-space:normal}
.zc{zoom:1!important}
}
@media screen{
html.tall .frame{width:auto!important;height:auto!important;overflow:visible!important}
html.tall .sheet{position:static!important;width:auto!important;height:auto!important;transform:none!important;max-width:1560px!important;margin:0 auto!important;padding:0 44px!important}
html.tall .frame + .frame{margin-top:40px}
html.tall .zc{zoom:1!important;display:contents}
html.tall .md,html.tall .ctb,html.tall .bk{break-inside:avoid}
}
'''
head += f'<style id="pp-css">{CSS}</style>'

# ---- pieces of the template body
body0 = tpl[tpl.find('<body>') + 6: tpl.find('<div id="frame">')]
crops_a = tpl.find('<div class="crop"'); crops_b = tpl.find('<header')
CROPS = tpl[crops_a:crops_b]
i = tpl.find('<div class="noprint m-btns"'); j = tpl.find('</div>\n', tpl.find('<span>print</span>', i)) + 7
BTNS = tpl[i:j]
BTNS = re.sub(r'<a href="plaits-navigator\.pdf".*?</a>\n', '', BTNS, flags=re.S)
assert 'pdf' not in re.sub(r'<svg.*?</svg>', '', BTNS, flags=re.S), 'pdf link still there'
tail_a = tpl.find('<script>(function(){var r=document.documentElement,K="hn-mode"')
TAIL = tpl[tail_a: tpl.find('</body>')]

def stat(cls, label, acc=False):
    return (f'<div style="padding: 7px 10px; border-right: 2px solid {INK}; border-bottom: 2px solid {INK}; display: flex; align-items: baseline; gap: 10px">'
            f'<span class="{cls}" style="font-family: \'Archivo\', sans-serif; font-weight: 900; font-size: 30px; line-height: 1; letter-spacing: -.02em; color: {ACC if acc else INK}">—</span>'
            f'<span style="font-family: \'Roboto Mono\', monospace; font-size: 10px; color: {MUTE}; white-space: nowrap">{label}</span></div>')

def header(n):
    return f'''<header style="padding-top: 30px; display: flex; flex-direction: column; gap: 14px">
<div class="m-slugs" style="display: flex; justify-content: space-between; font-family: 'Roboto Mono', monospace; font-size: 10.5px; line-height: 1.45; color: {INK}">
<div style="display: flex; flex-direction: column"><span style="font-weight: 600">plaits-palette-navigator ....... 00.{n:02d}_01</span><span>palette ................... <span class="pp-name">no palette loaded</span></span></div>
<div class="tm-line" style="display: flex; flex-direction: column; align-items: center"><span><a class="tm" href="https://mellotom.github.io/travelers-guide/" style="display: inline-flex; align-items: center; gap: 5px"><svg width="14" height="9" viewBox="0 0 14 9" aria-hidden="true" style="display:block;flex:none"><path d="M13.2 4.5 H1.6 M5.1 1 L1.6 4.5 L5.1 8" fill="none" stroke="currentColor" stroke-width="1.3"></path></svg><span>return to welcome center</span></a></span><span>mode ....................... <button type="button" class="tm" data-t="native" aria-pressed="false">light</button>/<button type="button" class="tm" data-t="alt" aria-pressed="false">dark</button></span><span class="vw-line">view ............. <button type="button" class="tm" data-v="sheet" aria-pressed="false">sheet</button>/<button type="button" class="tm" data-v="scroll" aria-pressed="false">scroll</button></span></div>
<div style="display: flex; flex-direction: column; text-align: right; position: relative"><span>source ............ <a href="https://rubato.audio/plaits-palette/" target="_blank" rel="noopener" style="{U}">rubato audio plaits palette</a></span><span>catalog pulled ............ {PULLED}</span>{'<span class="gc" data-l="40" style="position: absolute; right: 0; top: 100%; white-space: nowrap; visibility: hidden">visitors</span>' if n == 1 else ''}</div>
</div>
<div class="m-hgrid" style="display: grid; grid-template-columns: minmax(0, 1fr) 720px; gap: 56px; align-items: end">
<div style="display: flex; flex-direction: column; gap: 12px; min-width: 0">
<div class="m-titlerow" style="display: flex; align-items: flex-end; gap: 28px">
<{'h1' if n == 1 else 'div'} class="m-h1" style="margin: 0; font-family: 'Archivo', sans-serif; font-weight: 900; font-size: 124px; line-height: .8; letter-spacing: -.035em; white-space: nowrap">plaits palette</{'h1' if n == 1 else 'div'}>
<div class="m-sub" style="display: flex; flex-direction: column; gap: 3px; padding-bottom: 2px; font-family: 'Archivo', sans-serif; font-weight: 900; font-size: 32px; line-height: .95; letter-spacing: -.02em"><span>_travelers guide</span><span style="color: {ACC}">_for decoding the voice index</span></div>
</div>
<div style="height: 14px; background: {INK}"></div>
</div>
<div style="display: flex; flex-direction: column; gap: 10px">
<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); border-top: 2px solid {INK}; border-left: 2px solid {INK}">{stat('pp-st-models', 'models in this build')}{stat('pp-st-banks', 'banks of eight')}{stat('pp-st-tables', 'chord tables', True)}</div>
<div style="display: flex; flex-wrap: wrap; gap: 6px 18px; font-family: 'Roboto Mono', monospace; font-size: 11px; color: var(--c4A433D); align-items: baseline"><span><span class="b">[ left ]</span> press</span><span><span class="b h">[ left ]</span> hold</span><span>› then</span><span>twist = the fourth control, on frequency</span></div>
</div>
</div>
</header>
<div class="m-stripes" style="display: flex; flex-direction: column; gap: 3px; margin: 16px -64px 0" aria-hidden="true"><div style="height: 3px; background: #4F9B6A"></div><div style="height: 3px; background: #C9534F"></div><div style="height: 3px; background: #D69B35"></div><div style="height: 3px; background: #DD6E37"></div><div style="height: 3px; background: #D6B635"></div><div style="height: 3px; background: {ACC}"></div><div style="height: 3px; background: {MUTE}"></div><div style="height: 3px; background: {INK}"></div><div style="height: 3px; background: #5A5A5A"></div></div>
'''

def strip(a, b, c):
    return (f'<div class="m-strip" style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid {INK}; font-family: \'Roboto Mono\', monospace; font-size: 10.5px; color: {MUTE}">'
            f'<span>{a}</span><span>{b}</span><span style="color: {ACC}">{c}</span></div>')

def footer(n, cols):
    return f'''<footer class="m-footer" style="margin-top: 12px; margin-bottom: 24px; height: 50px; display: grid; grid-template-columns: {cols}; column-gap: 28px; font-family: 'Roboto Mono', monospace; font-size: 10.5px; line-height: 1.5; color: {MUTE}">
<div style="grid-column: 1 / span 4; border-top: 4px solid {INK}; display: flex; align-items: center"><span>design homage to the <a href="https://www.marvel.com/comics/guides/1556/house-of-xpowers-of-x" target="_blank" rel="noopener" style="{U}">house of x / powers of x</a> data pages — designed by tom muller with jonathan hickman · model descriptions from the <a href="https://rubato.audio/plaits-palette/" target="_blank" rel="noopener" style="{U}">rubato audio plaits palette</a> catalog<br>not affiliated with rubato audio, mutable instruments or marvel</span></div>
<div style="display: flex; flex-direction: column; align-items: flex-end; justify-content: center; padding-top: 4px; color: {INK}; white-space: nowrap"><span style="display: block">conceived by&nbsp;<a href="https://linktr.ee/mellotom" target="_blank" rel="noopener" style="{U}">mellotom</a>&nbsp;· plaits-palette-navigator ... 00.{n:02d}_08</span><span style="display: block; opacity: .62">created with claude</span></div>
</footer>'''

def T(x, y, t, size=9, w=500, anchor='start', fill=INK):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="font-family: \'Roboto Mono\', monospace; font-size: {size}px; font-weight: {w}; fill: {fill}">{t}</text>'

# fig.01: where the file comes from (own drawing of the palette page layout)
f1 = ['<svg viewBox="0 0 400 190" style="width: 100%; height: auto; display: block" role="img" aria-label="the plaits palette page: save configuration is top right of arrange your palette, download firmware wav is bottom right">']
f1.append(f'<rect x="1" y="1" width="296" height="188" style="fill: none; stroke: {INK}; stroke-width: 1.2"></rect>')
f1.append(f'<rect x="304" y="1" width="95" height="188" style="fill: none; stroke: {INK}; stroke-width: 1.2"></rect>')
f1.append(T(10, 18, 'arrange your palette', 10, 700))
f1.append(T(312, 18, 'model library', 9.5, 700))
f1.append(f'<rect x="150" y="7" width="64" height="16" rx="8" style="fill: none; stroke: {MUTE}; stroke-width: 1"></rect>' + T(182, 18, 'open config…', 7.5, 500, 'middle', MUTE))
f1.append(f'<rect x="219" y="6" width="72" height="18" rx="9" style="fill: {ACC}; stroke: {ACC}"></rect>' + T(255, 18, 'save configuration', 7, 700, 'middle', '#FFFFFF'))
for bi, (nm, col) in enumerate([('green', '#4F9B6A'), ('red', '#C9534F'), ('amber', '#D69B35')]):
    x = 8 + bi * 96
    f1.append(f'<rect x="{x}" y="46" width="88" height="92" style="fill: none; stroke: {MUTE}; stroke-width: 1"></rect><circle cx="{x+8}" cy="55" r="3" style="fill: {col}"></circle>' + T(x + 15, 58, nm, 7.5, 600))
    for k in range(8):
        f1.append(f'<rect x="{x+5}" y="{63+k*9}" width="78" height="6.5" style="fill: var(--cDDD3C3)"></rect>')
f1.append(f'<rect x="8" y="144" width="88" height="34" style="fill: none; stroke: {MUTE}; stroke-width: 1"></rect><circle cx="16" cy="153" r="3" style="fill: #DD6E37"></circle>' + T(23, 156, 'orange', 7.5, 600))
for k in range(2):
    f1.append(f'<rect x="13" y="{161+k*8}" width="78" height="6" style="fill: var(--cDDD3C3)"></rect>')
for k in range(9):
    f1.append(f'<rect x="310" y="{28+k*14}" width="83" height="10" style="fill: var(--cDDD3C3)"></rect>')
f1.append(f'<rect x="306" y="160" width="91" height="15" rx="7.5" style="fill: none; stroke: {INK}; stroke-width: 1.2"></rect>' + T(351.5, 170.5, 'download firmware wav', 6.3, 600, 'middle'))
f1.append(f'<path d="M255 26 V36 H246" style="fill: none; stroke: {ACC}; stroke-width: 1.5"></path>' + T(242, 39, 'the file this page reads', 8, 700, 'end', ACC))
f1.append('</svg>')
FIG1 = ''.join(f1)

def figtitle(num, title, tag):
    return (f'<div style="display: flex; justify-content: space-between; align-items: baseline; border-top: 4px solid {INK}; padding-top: 6px">'
            f'<span style="font-family: \'Archivo\', sans-serif; font-weight: 900; font-size: 20px; letter-spacing: -.015em">__fig.{num} : {title}</span><span class="sc">{tag}</span></div>')

def b(x, h=False): return f'<span class="b{" h" if h else ""}">[ {x} ]</span>'

COL1 = f'''<div class="col" style="align-self: stretch">
<section class="sec">
<div class="sh"><span class="sn" style="background: #D6B635; color: #1F1B19">01</span><h2 class="st">load your palette</h2><span class="sc">plp_01</span></div>
<div class="r"><div class="kc"><span class="v">step 1</span></div><div class="a">on <a href="https://rubato.audio/plaits-palette/" target="_blank" rel="noopener">plaits palette</a>, press <b>save configuration</b>, top right of “arrange your palette”</div></div>
<div class="r"><div class="kc"><span class="v">step 2</span></div><div class="a">it saves a file ending in <b>.plaits-palette.json</b>. this is separate from <b>download firmware wav</b>, which doesn’t include it</div></div>
<div class="r"><div class="kc"><span class="v">step 3</span></div><div class="a">drop that file below. the guide to your firmware builds itself</div></div>
<div class="pp-drop" id="pp-drop"><input type="file" id="pp-file" accept=".json,application/json" hidden><button type="button" class="pp-btn go" id="pp-pick">choose your .plaits-palette.json</button><span class="v">or drag the file onto this box · nothing is uploaded, it is read in your browser</span></div>
<p class="pp-status" id="pp-status" role="status" aria-live="polite"></p>
<div class="pp-acts"><button type="button" class="pp-btn" id="pp-share" hidden>copy share link</button><button type="button" class="pp-btn" id="pp-dl" hidden>download config</button><button type="button" class="pp-btn" id="pp-clear" hidden>clear</button><button type="button" class="pp-btn" id="pp-stock">see the stock lineup</button></div>
<p class="note">once loaded, this browser remembers your palette. the share link opens the same guide on any device, no file needed.</p>
</section>
<section class="sec" style="gap: 8px">
{figtitle('01', 'where the file comes from', 'rubato.audio/plaits-palette')}
<div class="pp-fig">{FIG1}</div>
<div class="note" style="margin: 0">the .wav goes to the module · the .json comes here</div>
</section>
</div>'''
COL23 = f'''<div class="col" style="align-self: stretch; grid-column: span 2">
<section class="sec">
<div class="sh"><span class="sn" style="background: #4F9B6A; color: #1F1B19">02</span><h2 class="st">voice index</h2><span class="sc">plp_02 · bank · slot · LED</span></div>
<div class="bks" id="pp-index"></div>
</section>
</div>'''
COL4 = f'''<div class="col" style="align-self: stretch">
<section class="sec">
<div class="sh"><span class="sn" style="background: #C9534F; color: #1F1B19">03</span><h2 class="st">options menu</h2><span class="sc">plp_03</span></div>
<div class="r"><div class="kc">{b('left')}<i class="p">+</i>{b('right')} <span class="v">tap</span></div><div class="a">enter / exit. all eight lights are the menu: {b('left')} moves between lights, {b('right')} steps a light’s settings. colour = setting: green, red, yellow, then the same three blinking</div></div>
<div id="pp-opts"></div>
<div id="pp-notes"></div>
</section>
{BTNS}
</div>'''
PANEL = f'''<div class="m-panel" style="display: flex; flex-direction: column; background: var(--cEAE2D3); color: {INK}; border: 2px solid {INK}; padding: 0 26px 16px; min-width: 0; min-height: 0">
<div style="display: flex; flex-direction: column; gap: 2px; margin: 0 -26px 12px" aria-hidden="true"><div style="height: 4px; background: #4F9B6A"></div><div style="height: 4px; background: #C9534F"></div><div style="height: 4px; background: #D69B35"></div><div style="height: 4px; background: #DD6E37"></div><div style="height: 4px; background: #D6B635"></div></div>
<div class="m-figblock" style="flex: 1; min-height: 0; display: flex; flex-direction: column; gap: 8px">
<div style="display: flex; justify-content: space-between; align-items: baseline"><span style="font-family: 'Archivo', sans-serif; font-weight: 900; font-size: 27px; line-height: 1; letter-spacing: -.02em">__fig.02 : front panel</span><span class="sc">the module the palette runs on</span></div>
<div class="m-figrow" style="flex: 1; min-height: 0; display: flex; flex-direction: column-reverse; gap: 14px; padding-bottom: 6px">
<div class="m-legend" style="flex: none; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); column-gap: 24px">
<div class="r"><div class="kc"><span class="b">harmonics</span></div><div class="a">each model’s first control</div></div>
<div class="r"><div class="kc"><span class="b">timbre</span></div><div class="a">second control</div></div>
<div class="r"><div class="kc"><span class="b">morph</span></div><div class="a">third control</div></div>
<div class="r"><div class="kc"><span class="b">frequency</span></div><div class="a">pitch, or <b>twist</b> once light 3 is set to it</div></div>
<div class="r"><div class="kc"><span class="b">8 LEDs</span></div><div class="a">slot 1–8 in a bank · colour = bank: green, red, amber, orange</div></div>
<div class="r"><div class="kc"><span class="b">out · aux</span></div><div class="a">every model lists what each jack carries</div></div>
</div>
<div class="m-svgpanel" style="flex: 1; min-width: 0; min-height: 0; position: relative">{panel}</div>
</div>
</div>
</div>'''
G1 = 'repeat(4, minmax(0, 1fr)) minmax(0, 1.55fr)'
G2 = 'repeat(5, minmax(0, 1fr))'
SHEET1 = f'''<div id="frame">
<div id="sheet" style="position: absolute; top: 0; left: 0; width: 2560px; height: 1440px; transform-origin: 0 0; box-sizing: border-box; background: var(--cF3EDE2); color: {INK}; display: flex; flex-direction: column; padding: 0 64px">
{CROPS}{header(1)}{strip('a guide that writes itself from your palette file · every model, bank by bank', 'read in your browser · nothing uploaded · remembered here · share by link', 'orange = hold')}
<div class="m-grid" style="display: grid; grid-template-columns: {G1}; gap: 28px; padding-top: 14px; align-items: stretch; flex: 1; min-height: 0">
{COL1}
{COL23}
{COL4}
{PANEL}
</div>
{footer(1, G1)}
</div>
</div>
'''
SHEETN = f'''<div class="frame" id="frame__N__">
<div class="sheet" id="sheet__N__">
{CROPS}{header(0).replace('00.00_01', '00.0__N___01')}{strip('harmonics · timbre · morph · twist: what each one does on every model', 'out / aux: what each jack carries · trig: what a trigger does', 'descriptions: rubato audio')}
<div class="m-grid" style="display: grid; grid-template-columns: {G2}; gap: 28px; padding-top: 14px; align-items: start; flex: 1; min-height: 0">
<div class="col pm"></div><div class="col pm"></div><div class="col pm"></div><div class="col pm"></div><div class="col px"></div>
</div>
{footer(0, G2).replace('00.00_08', '00.0__N___08').replace('grid-column: 1 / span 4', 'grid-column: 1 / span 4')}
</div>
</div>'''

FIT = '''<script>
(function(){
  function all(){return [].slice.call(document.querySelectorAll('#frame,.frame'));}
  function fit(pw){
    var w=pw||window.__ew(), flow=!pw && (w<900 || __tallNow());
    all().forEach(function(F){var S=F.firstElementChild;if(!S)return;
      if(flow){S.style.transform='';F.style.width='';F.style.height='';return;}
      var k=w/2560;S.style.transform='scale('+k+')';F.style.width=w+'px';F.style.height=(1440*k)+'px';});
  }
  var s=document.getElementById('sheet'),bt=document.querySelector('.m-btns'),home=bt&&bt.parentNode,ph=document.createComment('buttons');
  if(bt)home.insertBefore(ph,bt);
  function place(desk){if(!bt)return;var mob=!desk&&(window.__ew()<900||__tallNow());
    if(mob&&bt.parentNode===home)s.appendChild(bt);else if(!mob&&bt.parentNode!==home)home.insertBefore(bt,ph);}
  window.addEventListener('resize',function(){fit();place();});fit();place();
  window.addEventListener('beforeprint',function(){place(true);});
  window.addEventListener('beforeprint',function(){fit(1056);});
  window.addEventListener('afterprint',function(){fit();});
})();
</script>'''
data = dict(models=models['models'], retired=models['retired'], dx7=dx7, stock=stock, pulled=PULLED, title=TITLE, sheetHtml=SHEETN)
DATA = '<script>window.__PP=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';</script>'
APP = '<script>' + open(os.path.join(HERE, 'app.js'), encoding='utf-8').read() + '</script>'
page = head + '</head>\n<body>' + body0 + SHEET1 + '<div id="pp-tail"></div>\n' + FIT + '\n' + TAIL.replace('</body>', '')
# data + app must run after the view/theme scripts exist but before the final resize: put them before the view-toggle script
vt = page.rfind('<script>document.querySelectorAll(".tm[data-v]")')
page = page[:vt] + DATA + '\n' + APP + '\n' + page[vt:] + '</body>\n</html>\n'
page = page.replace('plaits-navigator-dark.pdf', '').replace('plaits-navigator.pdf', '')
open(out, 'w', encoding='utf-8').write(page)
print('ok', len(page))

#!/usr/bin/env python3
"""
Roll the EBI-refined elevated hero/frame treatment across all lifecycle emails.
Idempotent: replaces CSS rules by selector + wraps the hero img in the matted frame.
"""
import re, pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
EM=ROOT/"emails"

HERO_WRAP=""".hero-wrap { margin: 34px 0 36px; }
.hero-frame { position: relative; background: linear-gradient(157deg,#F7F2E1 0%,#EFE8CF 100%); border-radius:20px; border:1px solid rgba(26,28,34,0.06); padding:15px 15px 5px 15px; box-shadow:0 2px 5px rgba(66,61,50,0.05),0 30px 66px rgba(66,61,50,0.15); }
.hero-plate { position: relative; background:#FCFAF0; border:1px solid rgba(166,124,0,0.34); border-radius:12px; padding:8px; }
.hero-cap { font-family:'DM Mono',ui-monospace,monospace; font-size:10.5px; letter-spacing:0.14em; text-transform:uppercase; color:#8a8578; padding:13px 5px 3px 5px; overflow:hidden; }
.hero-cap .hc-tick { display:inline-block; width:16px; height:2px; background:#A67C00; vertical-align:middle; margin-right:10px; }
.hero-cap .hc-mark { float:right; color:#C4AE68; letter-spacing:0.2em; }
.hero-frame.no-cap { padding-bottom: 15px; }"""
HERO_IMG=".hero-img { width:100%; border-radius:7px; display:block; box-shadow:0 4px 12px rgba(66,61,50,0.10); }"
PROMPTS=".prompts { margin: 32px 0; padding: 24px 28px; background: linear-gradient(158deg,#EEE8D0 0%,#E7E0C6 100%); border:1px solid rgba(26,28,34,0.06); border-radius: 16px; box-shadow:0 14px 34px rgba(66,61,50,0.07); }"
PAUSE=".pause-block { text-align: center; margin: 34px 0; padding:26px 28px; background:#FBF8EC; border-radius:16px; border-top:2px solid #A67C00; box-shadow:0 12px 30px rgba(66,61,50,0.06); }"
PAUSE_P=".pause-block p { font-size: 15px !important; color: #6E6857 !important; margin-bottom: 0 !important; line-height: 1.95 !important; letter-spacing:0.01em; }"

DANGLERS={'in','into','on','at','of','the','a','an','to','for','with','one','under',
          'beside','and','cool','soft','dark','warm','grey','kraft','quiet'}

def caption(alt):
    a=re.sub(r'^(A|An|The)\s+','',alt.strip())
    truncated=False
    if len(a)>60:
        a=a[:60].rsplit(' ',1)[0]
        truncated=True
    words=a.split(' ')
    while words and words[-1].lower().strip(',') in DANGLERS:
        words.pop(); truncated=True
    text=' '.join(words).rstrip(',').strip()
    if truncated: text+='…'
    return (text[0].upper()+text[1:]) if text else 'The moment'

def hero_repl(m):
    attrs=m.group(1)
    alt=re.search(r'alt="([^"]*)"', attrs)
    cap=caption(alt.group(1)) if alt else 'The moment'
    # normalize width down a touch to sit inside the mat+plate padding
    attrs=re.sub(r'width="\d+"', 'width="520"', attrs)
    return ('<div class="hero-wrap">\n      <div class="hero-frame">\n'
            '        <div class="hero-plate">\n'
            f'          <img class="hero-img"{attrs}>\n'
            '        </div>\n'
            f'        <div class="hero-cap"><span class="hc-mark">PULSE</span><span class="hc-tick"></span>{cap}</div>\n'
            '      </div>\n    </div>')

def refresh_captions(p):
    """Idempotent correction pass over already-elevated heroes: dark-luxe (product-shot)
    emails lose the caption band entirely (it only ever duplicated the PULSE mark);
    lifestyle emails get their caption recomputed with the fixed caption() algorithm."""
    h=p.read_text(); orig=h
    is_dark='hero-fade' in h
    m=re.search(r'<img class="hero-img"[^>]*alt="([^"]*)"', h)
    if not m: return False
    if is_dark:
        h=re.sub(r'[ \t]*<div class="hero-cap">.*?</div>\n', '', h, count=1)
        h=re.sub(r'<div class="hero-frame">', '<div class="hero-frame no-cap">', h, count=1)
    else:
        cap=caption(m.group(1))
        h=re.sub(r'(<div class="hero-cap"><span class="hc-mark">PULSE</span><span class="hc-tick"></span>).*?(</div>)',
                  lambda mm: mm.group(1)+cap+mm.group(2), h, count=1)
    if h!=orig:
        p.write_text(h); return True
    return False

def process(p):
    h=p.read_text(); orig=h
    # body ground layer (skip if already applied)
    if 'background-color:#EBE7D4;background-image:radial-gradient' not in h:
        h=h.replace('background-color:#EBE7D4;font-family',
                    "background-color:#EBE7D4;background-image:radial-gradient(120% 70% at 50% 0%, #F1EBD8 0%, #EBE7D4 52%, #E4DEC7 100%);font-family",1)
    # outer tables transparent so the ground shows
    h=h.replace('style="background-color:#EBE7D4;">','style="background-color:transparent;">')
    # CSS rules by selector
    h=re.sub(r'\.hero-wrap\s*\{[^}]*\}', HERO_WRAP, h, count=1)
    h=re.sub(r'\.hero-img\s*\{[^}]*\}', HERO_IMG, h, count=1)
    h=re.sub(r'\.prompts\s*\{[^}]*\}', PROMPTS, h, count=1)
    h=re.sub(r'\.pause-block\s*\{[^}]*\}', PAUSE, h, count=1)
    h=re.sub(r'\.pause-block p\s*\{[^}]*\}', PAUSE_P, h, count=1)
    # hero markup -> framed structure (only matches the un-framed original)
    h=re.sub(r'<div class="hero-wrap">\s*<img class="hero-img"([^>]*)>\s*</div>', hero_repl, h, count=1)
    if h!=orig:
        p.write_text(h); return True
    return False

def main():
    changed=0; heroes=0; refreshed=0
    for p in sorted(EM.glob("*.html")):
        if process(p):
            changed+=1
            if 'class="hero-frame"' in p.read_text(): heroes+=1
        if refresh_captions(p):
            refreshed+=1
    print(f"elevated {changed} emails; {heroes} now have framed heroes; {refreshed} captions refreshed")

if __name__=="__main__": main()

#!/usr/bin/env python3
"""
Apply the advisory board's consensus email edits (subjects + CTAs) to the email HTML.
Reads email-board-review.json (the workflow consensus). Idempotent-ish; logs every change.
Usage: python3 tools/apply-email-edits.py
"""
import re, json, pathlib, html
ROOT=pathlib.Path(__file__).resolve().parent.parent
EM=ROOT/"emails"

def esc(s): return html.escape(s, quote=False)

def apply_edit(p, new_subject, new_cta):
    h=p.read_text(); changed=[]
    if new_subject:
        ns=esc(new_subject.strip())
        m=re.search(r'(<div class="email-subject">)(.*?)(</div>)', h, re.S)
        if m and m.group(2).strip()!=ns:
            old=m.group(2).strip()
            h=h[:m.start()]+m.group(1)+ns+m.group(3)+h[m.end():]
            # also refresh <title>
            h=re.sub(r'(<title>Pulse — )(.*?)(</title>)', lambda t: t.group(1)+ns+t.group(3), h, count=1)
            changed.append(f'subject: "{old}" → "{new_subject.strip()}"')
    if new_cta:
        nc=esc(new_cta.strip())
        m=re.search(r'(<a[^>]*class="btn-pill"[^>]*>)(.*?)(</a>)', h, re.S)
        if m and m.group(2).strip()!=nc:
            old=m.group(2).strip()
            h=h[:m.start()]+m.group(1)+nc+m.group(3)+h[m.end():]
            changed.append(f'CTA: "{old}" → "{new_cta.strip()}"')
    if changed: p.write_text(h)
    return changed

def main():
    data=json.loads((ROOT/"email-board-review.json").read_text())
    edits=data.get("consensus",{}).get("email_edits",[])
    applied=0; missing=[]
    for e in edits:
        eid=e.get("id","")
        if not eid.startswith("email-"): eid="email-"+eid
        p=EM/f"{eid}.html"
        if not p.exists(): missing.append(eid); continue
        ch=apply_edit(p, e.get("new_subject",""), e.get("new_cta",""))
        if ch:
            applied+=1
            print(f"• {eid}")
            for c in ch: print(f"    {c}")
    print(f"\napplied edits to {applied} emails; {len(missing)} ids not found: {missing[:8]}")

if __name__=="__main__": main()

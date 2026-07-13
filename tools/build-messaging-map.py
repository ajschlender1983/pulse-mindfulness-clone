#!/usr/bin/env python3
"""
Build messaging-map.json for the writing-room workshop: the 4 message categories
(CTA / Tagline / Product / Benefits), each with the CURRENT live-site copy and the
NEW board-consensus approach side by side, plus the guardrails classified
green (do) / yellow (careful) / red (never).
"""
import json, pathlib, re
ROOT=pathlib.Path(__file__).resolve().parent.parent
def load(f, default=None):
    p=ROOT/f
    return json.loads(p.read_text()) if p.exists() else default

site=load("live-site-copy.json",{"lines":[]})
board=load("messaging-board.json",{})
emails=load("email-board-review.json",{})

CATS=[("cta","CTA","The ask: what a reader is invited to do."),
      ("tagline","Tagline","The line: the hook, the headline, the thing on the billboard."),
      ("product","Product","What Pulse is and does, the mechanism in words."),
      ("benefits","Benefits","What it gives back: the felt outcome, the proof.")]

# ---- CURRENT (from the live site) ----
current={c[0]:[] for c in CATS}
for ln in site.get("lines",[]):
    cat=ln.get("cat")
    if cat in current: current[cat].append({"text":ln["text"],"where":ln.get("where","")})

# ---- NEW (board consensus + applied edits + the presence-return language) ----
cons=(board.get("final",{}) or {}).get("consensus",{}) or board.get("consensus",{}) or {}
new={c[0]:[] for c in CATS}
def add(cat,text,where):
    if text and not any(x["text"]==text for x in new[cat]): new[cat].append({"text":text,"where":where})

# tagline: hero + consensus taglines + text-on-screen
for line in re.split(r'\n', str(cons.get("hero",""))):
    line=line.strip()
    if line: add("tagline",line,"hero")
for t in cons.get("taglines",[]):
    add("tagline",t.get("text",""),(t.get("category","") or "").split("—")[0].strip()[:26] or "tagline")
for t in cons.get("tos",[]):
    add("tagline",t,"on screen")
add("tagline","Be Here WOW","canon")
add("tagline","Here & Now Together","canon")
add("tagline","Three reasons to look down. Every other reason, you look up.","canon")
add("tagline","Pulse gives you rhythm. Rhythm gives you pause.","canon")
# product: positioning + wedge + the plain-object lines
if cons.get("positioning"): add("product",cons["positioning"],"positioning")
if cons.get("wedge"): add("product",cons["wedge"],"the wedge")
for p in ["A gold ring that knows nothing about you — on purpose.",
          "No screen, no scores, nothing to check, ever.",
          "A pulse instead of a ping.",
          "It taps. You look up. Here you are.",
          "Two minutes to set up — then the ring does the remembering."]:
    add("product",p,"object")
# cta: the offer + the applied email CTAs
if cons.get("offer"): add("cta",cons["offer"],"the offer")
for e in (emails.get("consensus",{}) or {}).get("email_edits",[]):
    if e.get("new_cta"): add("cta",e["new_cta"],e.get("id","").replace("email-",""))
add("cta","When would now be a good time?","hero / close")
# benefits: the presence-return language (the board's concrete returns)
for b in ["About four dinners a week, returned.",
          "A whole bedtime story, with all of you in the room.",
          "The first coffee, actually tasted.",
          "Not more footage — the same footage, at the speed of being here.",
          "The days stop blurring when you're in them.",
          "If you can recall one moment of coming back, it's working.",
          "The word that matters is reclaimable — those hours aren't spent, they're waiting.",
          "Nothing measured you. The only instrument was you."]:
    add("benefits",b,"return")

# ---- GUARDRAILS classified green/yellow/red ----
def level(g):
    t=g.lower(); head=t.split(".")[0].split("—")[0].split(":")[0]  # the leading clause
    # a positive imperative in the LEAD clause wins → green (a "do")
    if re.match(r'\s*(always|lead|say|speak|perform|prefer|keep|land|ration|clarity|the wedge is a different|the return is a felt|the flag is)', head) or "always" in head:
        return "green"
    # a flat prohibition → red (a "never")
    if re.match(r'\s*(never|no |don\'t|don’t|ban|kill|retire|avoid)', head) or re.search(r'\bnever\b', head):
        return "red"
    return "yellow"
guardrails=[{"text":g,"level":level(g)} for g in cons.get("guardrails",[])]

# ---- CORE MESSAGING (the guide, downstream of the advisors) ----
core=[
 {"k":"The category","v":"A mindfulness ring that brings you back to the present — anti-data, nearly screen-free, nothing to check. The one screen that exists is deliberate, not ambient."},
 {"k":"Positioning","v":cons.get("positioning","")},
 {"k":"The wedge","v":cons.get("wedge","")},
 {"k":"The promise","v":"Stop watching the movie of your mind. Start making the movie of your life — the same footage, at the speed of being here. It isn't only the phone: even with empty hands, you can be replaying, rehearsing, worrying, instead of living what's actually in front of you."},
 {"k":"The offer","v":cons.get("offer","")},
 {"k":"The ritual (rev. 2026-07-13)","v":"Pulse is a verb. Pulse is the rhythm: it gives you a rhythm, helps you find pause, and pause is what lets you build a ritual of presence out of it. The ring sends a vibration; you choose your intention, and the Pulse is the ritual that follows. The ritual can look like breath, focus, feeling fully, appreciation, connection, creativity, soften, serve, or smile — surrender, honesty and courage are held back pending advisory-board review (persona research flagged them as Seeker-specific, at risk of overreach in mass copy). Rate this to weigh in."},
 {"k":"The three reasons to look (new, 2026-07-13)","v":"There are only three reasons to look down at a screen with Pulse: to set your intention, to deepen your practice, or to find the others. Every other reason, you look up. The vocabulary stays pulses, never pings — you schedule your pulses the way you schedule a practice, not the way you dread a notification."},
 {"k":"The four pillars (new, 2026-07-13)","v":"Two frameworks underneath everything Pulse says. The Pulse Map is the five states a pulse can return you to: Presence, Peace, Power, Pleasure, Purpose. Core Radiance is the four-part definition of what a person is like once they're living from that map — connection to others and the planet; charged up by life; clarity of heart and mind; capacity to love and serve others. The map is where you go. Radiance is who you become by going there."},
 {"k":"The feeling arc","v":"Numb → Seen → Hopeful → Convinced → Relieved → Grateful → Generous."},
 {"k":"The voice","v":"Present tense, second person, one breath per sentence. Invite, never instruct. No exclamation points."},
 {"k":"Canon lines","v":"When would now be a good time? · Be Here WOW · Here & Now Together · Three reasons to look down. Every other reason, you look up. · Pulse gives you rhythm. Rhythm gives you pause."},
]
core=[c for c in core if c["v"]]

# ---- MESSAGING HIERARCHY (first / second / third …) ----
ORD=["First","Second","Third","Fourth","Fifth","Sixth","Seventh"]
hierarchy=[]
for i,step in enumerate(cons.get("hierarchy",[])):
    s=str(step).strip()
    # strip a leading "First — " / "1." if present; we relabel ourselves
    s=re.sub(r'^(first|second|third|fourth|fifth|sixth|seventh)\s*[—:-]\s*', '', s, flags=re.I)
    hierarchy.append({"n":i+1,"label":ORD[i] if i<len(ORD) else str(i+1),"text":s})

out={"generated":"BUILD","categories":[{"id":c[0],"label":c[1],"blurb":c[2],
       "current":current[c[0]],"new":new[c[0]]} for c in CATS],
     "core":core, "hierarchy":hierarchy, "guardrails":guardrails,
     "counts":{"current":sum(len(v) for v in current.values()),"new":sum(len(v) for v in new.values()),
               "core":len(core),"hierarchy":len(hierarchy),"guardrails":len(guardrails)}}
(ROOT/"messaging-map.json").write_text(json.dumps(out,indent=1))
print("messaging-map.json:",out["counts"])
from collections import Counter
print("guardrail levels:",dict(Counter(g["level"] for g in guardrails)))
for c in out["categories"]: print(f"  {c['label']}: {len(c['current'])} current · {len(c['new'])} new")

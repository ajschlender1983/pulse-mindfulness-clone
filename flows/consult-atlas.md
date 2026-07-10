# ATLAS (CTO) — Port Instructions: opus-voice-flow-map.html → presence-flow-map.html

Line numbers refer to the source: `/Users/adamschlenderwork/dev/opus-os/projects/opus-pulse/public/opus-voice-flow-map.html` (5503 lines).

## 1. Architecture

Single-file port, no restructure. Script IIFE at 1364–5429 + optional Supabase bridge 5431–5500.

```
PulseMindfulness-Clone/
├── presence-flow-map.html            # ported app at repo root
├── emails/
│   ├── email-<slug>.html             # + sms-*.html, call-script-*.html, form-*, landing-*
│   └── images/hero-<slug>.png
└── tools/
    ├── generate-email-images.py
    └── email-image-manifest.json
```

**Invariant:** images relative to email (`src="images/hero-<slug>.png"`), emails relative to flow map (`"emails/email-<slug>.html"`), ZERO absolute paths. Works via http.server from root, inside the iframe, as file://, and under any subpath.

## 2. assetRefs resolution — exact change

Only consumer is `openAssetViewer()` (4280). Lines 4285–4292 strip `/public/`, force a leading slash (4286 — must delete), and add a `pulse.feelopus.com` host branch (4290–4292 — delete). Replace all of it with `var cleanUrl = url;`. `cleanUrl` feeds `openFull.href` (4297) and `frame.src` (4298). Drafts keyed by absolute `frame.src` (4334) — fine.

`guessAssetType()` (1402–1411) keys icons off filename prefixes `sms-`, `call-script`, `social-`, `form-`, `landing-` — keep those prefixes in new filenames; replace the `'threshold'` literal check (1409). Case-link at 4018 points to `/public/opus-admin.html#cases` — dead once Supabase is stripped (guard at 4015–4022 no-ops when `_tpCaseRefMap` empty).

## 3. localStorage + hardcoded identifiers (complete find→replace)

| Line | Current | New |
|---|---|---|
| 3202 | `LS_KEY = 'opus-flows-v1'` | `'pmf-flows-v1'` |
| 3203 | `LS_KEY_OLD = 'opus-campaigns-v1'` | delete + delete migration branch 3209–3215 |
| 3228 | `FLOW_STATE_KEY = 'opus-flow-state-v1'` | `'pmf-flow-state-v1'` |
| 4418 | `DRAFTS_KEY = 'opus-drafts-v1'` | `'pmf-drafts-v1'` |
| 4744 | `ACTIVE_PERSONA_KEY = 'opus-av-persona-v1'` | `'pmf-av-persona-v1'` |
| 4745 | `HIDE_SUGGESTIONS_KEY = 'opus-av-hide-suggestions-v1'` | `'pmf-av-hide-suggestions-v1'` |
| 5007 | `TEST_RECIPIENT_KEY = 'opus-av-test-recipient-v1'` | `'pmf-av-test-recipient-v1'` |
| 5008 | `LAST_CASE_ID_KEY = 'opus-av-last-case-id-v1'` | `'pmf-av-last-case-id-v1'` |
| 5395–5410 | `'opus-migration-v1'` / `'opus-reviewed-v1'` migration block | delete whole block |
| 5419–5422 | Reset button removes old `opus-*` literals | update to the NEW key names or Reset silently breaks |

| Line(s) | Current | Action |
|---|---|---|
| 6 | title "OPUS — Flow Map" | "Pulse — Cadence" |
| 1117 | topbar brand "OPUS Voice" | "Pulse · Cadence" |
| 1122–1125 | links index.html/hub.html/pulse.html/session-editor.html | repoint: index.html, presence-quiz.html, presence-experience.html, builds.html |
| 1248/1257 | "Pulse Rail" / "Pulse Brain · Merge Tags" | keep names deliberately (fits brand) |
| 4694, 4706–4739 | persona fixtures (SoundBed copy, feelopus URLs) | rewrite for Pulse personas + merge-tag ctx |
| 4317 | phase default `'Convinced'` | keep `'Convinced'` (exists in new arc) |
| 5136, 5151–5152 | `@feelopus\.com` test-send allowlist | `@pulsemindfulness\.com` |
| 5180 | fallback subject 'OPUS Voice Test' | 'Pulse Cadence Test' |
| 5431–5500 | **OPUS production Supabase URL + anon key + realtime bridge** | **EXCISE ENTIRELY** (guards at 5100/5196 no-op cleanly) |
| 3176 | seeded template bodyHtml (full OPUS email) | replace with Pulse template content |
| 4802–4811 etc. | `opus-cm-*` ids, `data-opus-orig-*`, `_opusLoadBound` | rename to `pmf-*` in one hygiene pass |

## 4. Email build strategy

43 distinct assets → 33 emails + 4 SMS + 2 call scripts + form/social/landing. One skeleton but unique per-email structure (dual-CTA forks, prompts boxes, art blocks, mailto subject routing). **Adapt each email individually**: (1) one golden reference converted by hand; (2) a token kit (color map, footer, signature, mailto, image scheme, voice); (3) parallel agents, one per email, preserving block structure 1:1.

QA gates:
```bash
# 1 Brand-leak grep — ZERO lines:
grep -rniE 'opus|soundbed|sound bed|feelopus|schenk|vibroacoust|transducer|threshold|528hz|album-art|soundtemple|netlify\.app|voice@' emails/ presence-flow-map.html
# 2 No external/absolute srcs in emails — ZERO:
grep -rnE 'src="(https?:|/)' emails/*.html
# 3 Every assetRef resolves (server from repo root):
grep -o '"url": "[^"]*"' presence-flow-map.html | cut -d'"' -f4 | while read u; do curl -sf -o /dev/null "http://localhost:8842/$u" || echo "MISSING: $u"; done
```
"session"/"frequencies" are legitimate mindfulness vocabulary — review by eye, don't ban. Also `grep -c cm-placeholder` per file should match source counts.

## 5. Image pipeline

Reuse generate-journey-images.py harness (auth 27–34, model autopick 46–68, retries/backoff + 3 config shapes 71–103, 1s sleep, gallery). Replace FRAMES (136–185) with json.load of manifest `[{"slug","prompt","aspect","use_ref"}]`; output `emails/images/hero-{slug}.png`; keep `--only <slug>`. **Add skip-if-exists guard** in the frame loop. Serial + 1s sleep is correct (10–20 RPM caps). ~35 images ≈ 10–25 min; budget 30.

## 6. Top silent-break risks

Phase-name string sites (coordinated single-pass edit):
1396 TRUST_SCORES keys · 1227–1235 avMetaPhase select options (written back at 4407) · SEEDED_FLOWS every `touchpoint.phase` + 69 hardcoded `phaseColor` hexes · 1455/1802/2190 `flow.phases` arrays (lowercase, data-only, never read by render) · 3465–3467 `TRUST_SCORES[tp.phase]` + `tp.phaseColor` · 3662–3670 renderTrustArc local TRUST_PHASES (own names + own hexes) · 3694–3701 flowPhases display map keyed by FLOW IDS · 3996–3997 detail panel · 4317 default.

Three independent phase color sources (touchpoint phaseColor, TRUST_PHASES hexes, flowPhases text) — align all three.

Risks + catches:
1. **Flow-id mismatch** — new ids must match: LINEAR_FLOWS (3194), SEPARATE_FLOWS (3195), flowPhases keys (3694–3701), flowOrder (3744), fallback `'resolution'` (3757, 5412), saveUserFlows filter `f.id !== 'resolution'` (3222), separator trigger `'session-drop'` (3762). Catch: fresh-profile load, click every trust-bar segment; grep old ids outside SEEDED_FLOWS → empty.
2. **Phase-key mismatch (case-sensitive)** — `TRUST_SCORES[tp.phase]` silently undefined. Catch: console assert all touchpoint phases exist as keys; diff select options vs Object.keys.
3. **Stale localStorage hydration** — init 5344–5394 merges saved state over seeds. Catch: rename all keys; verify in clean profile; verify Reset removes NEW keys.
4. **Asset URL mangling** — resolver must be gutted (see §2). Catch: curl loop + manual edit→save-draft→reopen round-trip (draft keyed on frame.src 4334).
5. **Live Supabase bleed** — excise 5431–5500; confirm network tab shows zero requests to *.supabase.co / *.feelopus.com.

Bonus: `?highlight=<tpId>` deep link (3951–3963) — test one id end-to-end after reseeding.

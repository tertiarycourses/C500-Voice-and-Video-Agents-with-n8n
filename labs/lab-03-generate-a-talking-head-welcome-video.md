# Lab 3 — Generate a Talking-Head Welcome Video

**Course:** Voice and Video Agents with n8n (C500)  
**Version:** v1.0  
**Release date:** 11 August 2026  
**Topic 2:** Video Agent  
**Maps to:** LO3: Build and verify a two-phase n8n avatar-video workflow that binds human approval to an exact script hash before one asynchronous render.  
**Tools:** n8n Webhook, AI Agent, OpenAI Chat Model, Code, HTTP Request, HeyGen API, Wait, IF, Respond to Webhook, browser Video Studio

**Suggested duration:** 55 minutes  
**Prerequisites:**
- Labs 1 and 2 are complete and the approved HarbourStay service facts are available as synthetic source material.
- A learner-owned OpenAI model credential and HeyGen API credential are stored in n8n; no secret appears in exported JSON.
- An authorised HeyGen avatar ID and voice ID are available, with quota for one short 1280x720 training render.
- Python 3 is available to serve labs/apps/video-studio; on Windows, py -m http.server is an equivalent fallback.

---

## Goal

Generate a synthetic HarbourStay script draft, approve that exact hashed draft, and receive one completed talking-head video URL with a traceable provider job ID.

## What You Will Do

You build a two-phase avatar-video workflow. A draft request turns approved facts into structured copy and returns the script plus its SHA-256 hash without calling HeyGen. A separate render request supplies the exact approved script and hash; n8n recomputes the hash, binds it to an authorised campaign profile, creates one video job and polls only that known job. A status-only starter lets an operator resume after the polling deadline without creating again.

## What You Will Build

A draft-and-render n8n webhook, a browser Video Studio that preserves the reviewed script snapshot, one authorised 16:9 captioned avatar video, a status-only resume workflow, and redacted evidence linking brief, script hash, profile version, video ID, attempts and terminal state.

> **Data note.** Use only synthetic HarbourStay data, voices, avatars, bots and channels that you are authorised to use. Keep secrets in n8n credentials, disclose synthetic media, and do not publish a generated asset outside the private training channel.

## Steps

**1. Copy the evidence template to evidence/lab03-avatar-video.md. Record only synthetic content, hash and provider-ID suffixes; never paste complete credentials or private provider responses.**

```text
# Windows PowerShell
Copy-Item labs\evidence-template.md evidence\lab03-avatar-video.md

# macOS / Linux / WSL2
cp labs/evidence-template.md evidence/lab03-avatar-video.md
```

**2. Import the supplied workflow and rename it C500 Lab 03 - Avatar Video. Confirm Avatar Video Webhook uses POST path c500-avatar-video and Respond to Webhook. Copy its Test URL.**

```text
labs/workflows/lab03-avatar-video.json
POST /webhook-test/c500-avatar-video
```

**3. Open Validate Request. Confirm action must be draft or render. Draft requires brief_id, audience, objective, approved_facts, call_to_action and max_words 30-90. Render requires brief_id, approved_script, approved_script_hash, approved_disclosure and approved_for_render true.**

```text
action: draft | render
draft max_words: 30..90
render approved_for_render: true
```

**4. Inspect Is Draft Request. Its true path alone reaches Script Agent; its false path goes directly to Validate Approved Draft. There must be no path from a render request back through the model.**

```text
draft -> Script Agent
render -> Validate Approved Draft
render -> Script Agent: forbidden
```

**5. Attach a learner-owned OpenAI Chat Model to Script Agent. Keep its contract: use only approved_facts and return title, spoken_script, caption, claim_list and disclosure; do not invent prices, availability, testimonials or guarantees.**

```text
Output: title, spoken_script, caption, claim_list, disclosure
```

**6. Inspect Build Draft Snapshot and Hash Draft Script. Confirm the Code node extracts JSON even when the model wraps it in backtick or tilde fences, checks word count and claim subset, and requires disclosure. The native n8n Crypto node then writes a SHA-256 script_hash over the exact spoken_script without Code-node module imports.**

```text
script_contract_ok = true
Hash Draft Script: SHA256(exact spoken_script) -> script_hash
```

**7. Open Return Draft. Confirm it returns status draft_ready, brief_id, exact spoken_script, script_hash, caption, disclosure, claim_list and profile_id. It must not run Campaign Profile or Create Avatar Video.**

```text
Expected draft status: draft_ready
Expected HeyGen create calls: 0
```

**8. Open Video Studio through a local server, paste the Test URL and click Generate Draft. If python is unavailable on Windows, use the py fallback. Keep the n8n workflow listening.**

```text
python -m http.server 8001 --directory labs/apps/video-studio
# Windows fallback
py -m http.server 8001 --directory labs/apps/video-studio

Open http://localhost:8001
```

**9. Review the displayed script, disclosure and hash. Use only the Approve Exact Draft & Render button; it must send the stored spoken_script, disclosure and script_hash without asking the model for another script.**

```text
action = render
approved_script = exact draft text
approved_script_hash = displayed SHA-256
approved_disclosure = exact draft disclosure
approved_for_render = true
```

**10. Before a paid render, change one character in approved_script with browser developer tools or an API client while keeping the old hash. Confirm Hash Approved Script and Approval Snapshot Valid route to approval_mismatch and Create Avatar Video does not run.**

```text
Expected: approval_mismatch
Expected HeyGen create calls: 0
```

**11. Open Campaign Profile. Replace <HEYGEN_AVATAR_ID> and <HEYGEN_VOICE_ID> with authorised assets. Keep profile_version c500-demo-1, width 1280, height 720, captions true and destination private-preview.**

```text
avatar_id = <HEYGEN_AVATAR_ID>
voice_id = <HEYGEN_VOICE_ID>
profile_version = c500-demo-1
```

**12. Select an n8n HTTP Header Auth credential for HeyGen with header X-Api-Key in Create Avatar Video and Check Video Status. Confirm Create uses the exact approved_script followed by the approved synthetic-media disclosure, authorised IDs, 1280x720 dimensions and captions.**

```text
POST https://api.heygen.com/v2/video/generate
Header: X-Api-Key from n8n credential
voice.input_text = approved_script + approved_disclosure
```

**13. Inspect both HTTP nodes. Continue On Fail or the error output must route provider errors to Normalise Provider Error, which returns review_required with error_class and any known video_id rather than stopping before evidence is written.**

```text
create/status error -> Normalise Provider Error -> Return Provider Error
```

**14. Click Approve Exact Draft & Render once. Confirm Store Job records brief_id, approved_script_hash, approved_disclosure, profile_version, returned video_id, poll_attempt 0 and created_at before Wait. Never retry Create Avatar Video.**

```text
Expected create calls: 1
Required stored fields: video_id and approved_disclosure
poll_attempt = 0
```

**15. Trace Wait for Render, Check Video Status and Route Status. Processing increments poll_attempt and returns to Wait; completed returns the URLs; failed and the 20-attempt deadline return review_required while preserving the known video_id.**

```text
Wait: 15 seconds
Maximum status attempts: 20
processing -> Wait; never -> Create
```

**16. If the deadline is reached, import C500 Lab 03 - Status Resume, set Known Job.video_id to the retained value, select the HeyGen credential and run it. Confirm this workflow contains no create endpoint and performs status checks only.**

```text
labs/workflows/lab03-status-resume.json
GET /v1/video_status.get?video_id=<known video_id>
Create endpoint count: 0
```

**17. For a completed job, compare the rendered speech and captions with the exact approved_script; confirm authorised avatar, voice, 16:9 framing, disclosure and no unsupported claim. Record discrepancies as review_required.**

```text
Release evidence: script hash, identity, voice, captions, framing, disclosure
```

**18. Activate the main workflow and replace the Video Studio URL with its Production URL. Save a final node-by-node diff checklist in evidence: imported node names, changed credential selectors, avatar ID, voice ID, webhook URL, and no other structural changes.**

```text
POST /webhook/c500-avatar-video
Diff: credentials + authorised IDs + URL only
```

## Test It

Draft mode returns a valid structured script and SHA-256 hash with zero HeyGen calls. A changed script with the old hash fails closed. The exact approved snapshot creates one job, stores its video_id before bounded status polling, and ends completed or review_required without duplicate creation. A timed-out job can resume through the status-only workflow, and completed evidence binds the exact script hash, profile version, video ID and final asset without exposing credentials.

## Checkpoint

Keep the credential-free main and status-only workflows, authorised campaign profile, approved script snapshot and completed Lab 3 evidence. Rejoin here: import labs/workflows/lab03-avatar-video.json, select OpenAI and HeyGen credentials, set Campaign Profile, generate a fresh draft, approve that exact hash, then resume from Store Job using labs/workflows/lab03-status-resume.json only if a known video_id has timed out.

## Troubleshooting

- **The approved render produces a different script** — Stop: render requests must bypass Script Agent. Send the exact draft as approved_script and compare its recomputed SHA-256 with approved_script_hash before Campaign Profile.
- **Create Avatar Video returns an error** — Inspect Normalise Provider Error, compare the current official schema, confirm authorised IDs and preserve review_required evidence without retrying create.
- **Status remains processing beyond the lab** — Retain the original video_id and use lab03-status-resume.json; never submit the brief to the create endpoint again.
- **Video content differs from the snapshot** — Mark review_required, preserve both artefacts and create a separately approved new snapshot rather than editing evidence.

## Challenge

Add a second approved 1080x1920 campaign profile. Bind its version into the approval snapshot and prove an unknown profile or mismatched version fails before the create call.

## Reflection

Which exact values must be frozen at approval so a later render is demonstrably the media a reviewer authorised?

---

[← Lab 2](lab-02-connect-the-concierge-to-telegram-voice-notes.md) · [Lab 4 →](lab-04-automate-a-governed-video-campaign-pipeline.md)

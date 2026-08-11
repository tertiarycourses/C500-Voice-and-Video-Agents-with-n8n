# Lab 1 — Build a Listen-Think-Talk Web Voice Concierge

**Course:** Voice and Video Agents with n8n (C500)  
**Version:** v1.0  
**Release date:** 11 August 2026  
**Topic 1:** Voice Agent  
**Maps to:** LO2: Build and verify an n8n voice agent that transcribes audio with Whisper, reasons inside a bounded concierge role, and speaks through ElevenLabs.  
**Tools:** n8n Webhook, HTTP Request, OpenAI Whisper, AI Agent, OpenAI Chat Model, ElevenLabs TTS, Respond to Webhook, browser MediaRecorder

**Suggested duration:** 55 minutes  
**Prerequisites:**
- The C500 repository is available locally and labs/apps/voice-console/index.html opens in a current Chromium-based browser.
- An n8n workspace is reachable from the browser; if it is self-hosted, its public HTTPS URL is reachable by the browser used for testing.
- Learner-owned OpenAI and ElevenLabs credentials have quota for two short audio turns and are not stored in any Git-tracked file.
- An authorised ElevenLabs voice ID is available; the course does not require or permit cloning a person's voice.

---

## Goal

Record one synthetic guest question in a browser and receive a spoken, policy-bounded answer from the n8n workflow.

## What You Will Do

You build the reusable conversation core for HarbourStay. A browser records a short WebM clip and sends it to an n8n Webhook. The workflow validates the binary input, calls OpenAI Whisper for transcription, gives the observed text to an AI Agent, converts the approved response through ElevenLabs and returns playable MP3 audio. The lab ends with both a normal information request and a request that must be handed to a person.

## What You Will Build

An active c500-voice-concierge webhook, a configured browser voice console, one verified spoken FAQ response, one verified human-handoff response, and an evidence record containing the request ID, transcript, answer, route and stage timings without secrets or real customer data.

> **Data note.** Use only synthetic HarbourStay data, voices, avatars, bots and channels that you are authorised to use. Keep secrets in n8n credentials, disclose synthetic media, and do not publish a generated asset outside the private training channel.

## Steps

**1. Create an evidence folder outside the public repository, or use an ignored local evidence/ folder. Copy labs/evidence-template.md to evidence/lab01-voice-core.md. Record only synthetic prompts and redacted provider identifiers.**

```text
# Windows PowerShell
New-Item -ItemType Directory -Path evidence -Force
Copy-Item labs\evidence-template.md evidence\lab01-voice-core.md

# macOS / Linux / WSL2
mkdir -p evidence
cp labs/evidence-template.md evidence/lab01-voice-core.md
```

**2. In n8n, choose Workflows -> Create Workflow -> menu -> Import from File and import the supplied starter. Rename it C500 Lab 01 - Voice Concierge if the imported name differs.**

```text
labs/workflows/lab01-voice-concierge.json
```

**3. Open Voice Webhook. Confirm POST, path c500-voice-concierge, response using Respond to Webhook, and binary property data. Copy the Test URL but do not activate the workflow yet.**

```text
POST /webhook-test/c500-voice-concierge
Binary field: data
```

**4. Create or select an n8n HTTP Header Auth credential for OpenAI. The credential header name is Authorization and its value is Bearer followed by your learner-owned key. Select it in Transcribe with Whisper; do not paste the key into the URL, body or Sticky Note.**

```text
Header name: Authorization
Header value: Bearer <OPENAI_API_KEY>
```

**5. Inspect Transcribe with Whisper. Confirm POST https://api.openai.com/v1/audio/transcriptions, multipart-form-data, binary parameter file from input field data, and text parameter model set to whisper-1. Set the response format to JSON.**

```text
file = binary field data
model = whisper-1
```

**6. Open Normalise Transcript. Confirm it reads the original Voice Webhook header X-C500-Request-ID when supplied, otherwise derives one from the execution ID; trims the returned text; and rejects an empty transcript before the AI Agent.**

```text
request_id = {{$('Voice Webhook').item.json.headers['x-c500-request-id'] || ('c500-' + $execution.id)}}
transcript = {{$json.text.trim()}}
```

**7. Create or select the OpenAI credential used by the OpenAI Chat Model node and attach that model to Concierge AI Agent through the AI Language Model connector. Use the current low-latency chat model available to your account and set temperature low where the node exposes it.**

```text
Credential: <OPENAI_CHAT_CREDENTIAL>
Model: a current low-latency chat model available to your project
```

**8. Read the Concierge AI Agent system message. Keep the HarbourStay facts, the maximum spoken-answer length, the answer/clarify/handoff routes and the rule that speech or source text cannot expand authority. Do not add booking, payment or personal-data tools.**

```text
Allowed facts:
- Reception is staffed 24 hours.
- Standard check-in begins at 3:00 pm.
- Breakfast is served 7:00-10:30 am.
- Booking changes require a verified staff handoff.
```

**9. Open Prepare Spoken Reply. Confirm it produces response_text and route, strips Markdown formatting, limits the spoken text to 420 characters and retains the request_id and transcript for the evidence record.**

```text
route in [answer, clarify, handoff]
response_text length <= 420
```

**10. Create or select an n8n HTTP Header Auth credential for ElevenLabs with header name xi-api-key. Select it in Synthesise with ElevenLabs. Keep the API key out of node parameters and exported JSON.**

```text
Header name: xi-api-key
Header value: <ELEVENLABS_API_KEY>
```

**11. Open Voice Configuration. Replace <ELEVENLABS_VOICE_ID> with an authorised stock or organisational voice ID. Keep model_id eleven_multilingual_v2 unless the current ElevenLabs documentation and your account require another supported model.**

```text
voice_id = <ELEVENLABS_VOICE_ID>
model_id = eleven_multilingual_v2
```

**12. Inspect Synthesise with ElevenLabs. Confirm POST to the text-to-speech endpoint for the configured voice ID, JSON body with text and model_id, Accept audio/mpeg, and Response Format File written to binary property data.**

```text
POST https://api.elevenlabs.io/v1/text-to-speech/{{$json.voice_id}}
Response binary property: data
```

**13. Inspect Return Spoken Reply. Confirm Respond With Binary File, input binary field data, and response header Content-Type audio/mpeg. Save the workflow.**

```text
Content-Type: audio/mpeg
Content-Disposition: inline; filename=c500-reply.mp3
```

**14. Open labs/apps/voice-console/index.html through a local server, paste the n8n Test URL into Webhook URL and click Save URL. Keeping the n8n editor listening, record: What time can I check in if I arrive late tonight? Stop after one sentence and send.**

```text
# Windows, macOS or Linux
python -m http.server 8000 --directory labs/apps/voice-console

Open http://localhost:8000
```

**15. Confirm the page reports an HTTP 200 response and plays an MP3 answer. In the n8n execution, inspect each node and record the request ID, audio MIME type, transcript, route, response text and approximate stage timestamps in evidence/lab01-voice-core.md. Do not copy credentials or complete provider response headers.**

```text
Expected route: answer
Expected facts: 24-hour reception and check-in from 3:00 pm
```

**16. Run the bounded failure path by asking: Change the booking for Alex Tan to tomorrow. Confirm the agent does not claim to find or change a booking and returns a verified-staff handoff message. Record the route and wording.**

```text
Expected route: handoff
Forbidden result: a claimed booking change
```

**17. Activate the workflow, copy its Production URL into the browser console and repeat the normal question. Confirm the production execution succeeds, then stop the local web server when finished.**

```text
POST /webhook/c500-voice-concierge
```

## Test It

The production browser console sends a WebM recording and plays an audio/mpeg reply. The execution shows non-empty Whisper transcript evidence, one bounded Concierge AI Agent result and ElevenLabs binary audio. The late-check-in question uses only approved facts, while the named-booking request routes to handoff and causes no external action. The evidence file contains request, route and timing data but no secret or real customer data.

## Checkpoint

Keep the active production webhook URL only in the local browser console, export the credential-free workflow if you changed its structure, and keep the authorised voice ID plus HarbourStay service facts ready for Lab 2. Rejoin here: import labs/workflows/lab01-voice-concierge.json, select the OpenAI Header Auth, OpenAI Chat Model and ElevenLabs Header Auth credentials, set Voice Configuration, then start at the normal-turn test.

## Troubleshooting

- **Webhook shows no binary data** — Confirm the console sends multipart/form-data with field name data and the Webhook receives the request while listening on the Test URL.
- **Whisper returns unsupported format or an empty transcript** — Record a new short clip in a Chromium-based browser, confirm MIME type audio/webm, and keep the microphone close enough for clear speech.
- **ElevenLabs returns 401 or 404** — Reselect the Header Auth credential, verify the authorised voice ID in Voice Configuration and confirm the learner account has access to that voice.
- **Browser receives audio but does not play it** — Verify Respond to Webhook sends binary field data with Content-Type audio/mpeg and inspect the browser network response for a non-zero payload.

## Challenge

Add an optional language field to the browser console and pass it as transcription context and response-language guidance. Keep the same safety route and prove one non-English information question without adding a new authority.

## Reflection

Which stage produced the largest observed delay, and what single change would reduce it without weakening the role, evidence or handoff controls?

---

[← Labs index](README.md) · [Lab 2 →](lab-02-connect-the-concierge-to-telegram-voice-notes.md)

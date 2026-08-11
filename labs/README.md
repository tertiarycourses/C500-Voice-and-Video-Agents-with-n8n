# Voice and Video Agents with n8n (C500) — Hands-On Labs

4 labs across 2 topics · 1 day · 8 scheduled hours

Work through the labs in order — each one builds on the artifacts you produced in the labs before it.


## Topic 1 — Voice Agent

| # | Lab | Tools | You Build |
|---|-----|-------|-----------|
| 1 | [Build a Listen-Think-Talk Web Voice Concierge](lab-01-build-a-listen-think-talk-web-voice-concierge.md) | n8n Webhook, HTTP Request, OpenAI Whisper, AI Agent, OpenAI Chat Model, ElevenLabs TTS, Respond to Webhook, browser MediaRecorder | An active c500-voice-concierge webhook, a configured browser voice console, one verified spoken FAQ response, one verified human-handoff response, and an evidence record containing the request ID, transcript, answer, route and stage timings without secrets or real customer data. |
| 2 | [Connect the Concierge to Telegram Voice Notes](lab-02-connect-the-concierge-to-telegram-voice-notes.md) | n8n Telegram Trigger and Telegram nodes, OpenAI Whisper, AI Agent, Window Buffer Memory, ElevenLabs TTS, IF, chat and phone adapter design | An active Telegram voice-note concierge with a text-message help branch, bounded four-turn memory keyed to the chat, one verified spoken reply, one verified fallback, and phone-channel-map.md covering call event, media, session, response and transfer contracts. |

## Topic 2 — Video Agent

| # | Lab | Tools | You Build |
|---|-----|-------|-----------|
| 3 | [Generate a Talking-Head Welcome Video](lab-03-generate-a-talking-head-welcome-video.md) | n8n Webhook, AI Agent, OpenAI Chat Model, Code, HTTP Request, HeyGen API, Wait, IF, Respond to Webhook, browser Video Studio | A draft-and-render n8n webhook, a browser Video Studio that preserves the reviewed script snapshot, one authorised 16:9 captioned avatar video, a status-only resume workflow, and redacted evidence linking brief, script hash, profile version, video ID, attempts and terminal state. |
| 4 | [Automate a Governed Video Campaign Pipeline](lab-04-automate-a-governed-video-campaign-pipeline.md) | n8n Schedule Trigger, Manual Trigger, Data Table, Code, HeyGen API, Wait, IF, Telegram Send Video, persistent ledger, release runbook | A c500_campaign_queue approval table, c500_campaign_runs ledger, scheduled-but-disabled n8n pipeline, one privately distributed training video, a duplicate-skip trace, status-only recovery path and an operating runbook. |

---

> Use only synthetic HarbourStay data, voices, avatars, bots and channels that you are authorised to use. Keep secrets in n8n credentials, disclose synthetic media, and do not publish a generated asset outside the private training channel.


_Tertiary Infotech Academy Pte Ltd · C500 · v1.0 (11 August 2026)_

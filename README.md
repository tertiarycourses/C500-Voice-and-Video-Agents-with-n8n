<div align="center">

# Voice and Video Agents with n8n

[![Course](https://img.shields.io/badge/Course-C500-1f6feb?style=for-the-badge)](https://www.tertiarycourses.com.sg/voice-and-video-agents-with-n8n.html)
[![n8n](https://img.shields.io/badge/Built_with-n8n-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)](https://n8n.io)
[![Voice](https://img.shields.io/badge/Agent-Voice-0f766e?style=for-the-badge)](#lab-1--build-a-listen-think-talk-web-voice-concierge)
[![Video](https://img.shields.io/badge/Agent-Video-6d28d9?style=for-the-badge)](#lab-3--generate-a-talking-head-welcome-video)
[![License](https://img.shields.io/badge/Use-Educational-f59e0b?style=for-the-badge)](#educational-use)

**Concept-first courseware and connected n8n labs for building voice and avatar-video agents — from browser and Telegram audio to an asynchronous, governed video campaign pipeline.**

[Course page](https://www.tertiarycourses.com.sg/voice-and-video-agents-with-n8n.html) · [Learner Guide](LG-Voice%20and%20Video%20Agents%20with%20n8n%20%28C500%29.md) · [Labs](labs/README.md) · [Report an issue](https://github.com/tertiarycourses/C500-Voice-and-Video-Agents-with-n8n/issues)

</div>

> [!NOTE]
> These are the official learning materials for **Voice and Video Agents with n8n**, course code **C500**, by Tertiary Courses / Tertiary Infotech Academy.

## Course package

The repository is built from one shared content source so the topic order, learning outcomes, lab titles and verification steps stay aligned across:

- trainer slides and learner-slide PDF;
- Learner Guide in Word, PDF and Markdown;
- Lesson Plan in Word and PDF;
- four detailed lab files, importable n8n starters and two browser apps.

Generated documents are in [`courseware/`](courseware/). The learner-facing lab index is [`labs/README.md`](labs/README.md).

## Connected HarbourStay labs

### Lab 1 — Build a Listen-Think-Talk Web Voice Concierge

Browser microphone -> n8n Webhook -> Whisper transcription -> bounded AI Agent -> ElevenLabs speech -> playable MP3 response.

Start with [`labs/lab-01-build-a-listen-think-talk-web-voice-concierge.md`](labs/lab-01-build-a-listen-think-talk-web-voice-concierge.md), import [`lab01-voice-concierge.json`](labs/workflows/lab01-voice-concierge.json), then open the [`voice-console`](labs/apps/voice-console/).

### Lab 2 — Connect the Concierge to Telegram Voice Notes

Telegram voice-file adapter -> the same concierge role -> spoken reply, bounded memory, a text-message fallback and a documented telephone-channel contract.

Use [`labs/lab-02-connect-the-concierge-to-telegram-voice-notes.md`](labs/lab-02-connect-the-concierge-to-telegram-voice-notes.md) and [`lab02-telegram-voice-agent.json`](labs/workflows/lab02-telegram-voice-agent.json).

### Lab 3 — Generate a Talking-Head Welcome Video

Synthetic brief -> structured draft + SHA-256 -> exact human approval snapshot -> authorised HeyGen avatar profile -> create-once job -> bounded status polling -> verified video URL.

Use [`labs/lab-03-generate-a-talking-head-welcome-video.md`](labs/lab-03-generate-a-talking-head-welcome-video.md), [`lab03-avatar-video.json`](labs/workflows/lab03-avatar-video.json), the create-free [`lab03-status-resume.json`](labs/workflows/lab03-status-resume.json) and the [`video-studio`](labs/apps/video-studio/).

### Lab 4 — Automate a Governed Video Campaign Pipeline

n8n Data Table queue and persistent run ledger -> exact approval/hash/destination checks -> avatar-video render -> release checks -> disclosed private Telegram preview.

Use [`labs/lab-04-automate-a-governed-video-campaign-pipeline.md`](labs/lab-04-automate-a-governed-video-campaign-pipeline.md) and [`lab04-video-campaign-pipeline.json`](labs/workflows/lab04-video-campaign-pipeline.json).

## Architecture

```text
VOICE CORE
  Browser multipart audio / Telegram voice file
       -> validate binary media
       -> Whisper transcription
       -> bounded HarbourStay AI Agent
       -> ElevenLabs speech
       -> browser MP3 / Telegram audio

VIDEO PIPELINE
  Approved brief or campaign queue row
       -> structured script and claim checks
       -> authorised avatar campaign profile
       -> HeyGen create once -> store video_id
       -> wait -> status -> completed / failed / operator review
       -> release checks -> private distribution -> run ledger
```

## Getting started

1. Clone this repository and open the matching lab Markdown.
2. Import its JSON from [`labs/workflows/`](labs/workflows/).
3. Reselect only your learner-owned credentials in n8n; exported starters contain no usable secrets.
4. Keep media synthetic, clips short and destinations private.
5. Run the stated positive path and bounded failure path, then record redacted evidence with [`labs/evidence-template.md`](labs/evidence-template.md).

See the Learner Guide for concept explanations, provider contracts, troubleshooting, accessibility, consent, cost and deployment guidance.

## Project structure

```text
C500-Voice-and-Video-Agents-with-n8n/
├── README.md
├── LG-Voice and Video Agents with n8n (C500).md
├── courseware/                 # PPT/PDF, Learner Guide and Lesson Plan
├── labs/
│   ├── README.md               # aligned lab index
│   ├── lab-01-*.md ... lab-04-*.md
│   ├── workflows/              # credential-free n8n starter exports
│   ├── apps/                   # browser Voice Console and Video Studio
│   └── evidence-template.md
├── reference/                  # authoritative research links
└── .agents/skills/non-wsq-courseware-build/
    └── build/                  # single-source generators and content modules
```

## Safety and credentials

- Use only voices, avatars, bots, accounts, media and channels you are authorised to use.
- Disclose automated and synthetic media where viewers could otherwise be misled.
- Keep provider keys and bot tokens in n8n credential storage; never paste them into prompts, workflow exports, evidence or Git.
- Treat speech and external content as data, not authority to change roles, tools, approvals or destinations.
- Keep consequential account changes, payments, emergencies and public releases behind verified human control.

## Educational use

This repository is provided for educational use as part of course C500. © Tertiary Infotech Academy Pte Ltd. All rights reserved.

## Developed by

**Tertiary Infotech Academy Pte Ltd** — [Tertiary Courses](https://www.tertiarycourses.com.sg/voice-and-video-agents-with-n8n.html)

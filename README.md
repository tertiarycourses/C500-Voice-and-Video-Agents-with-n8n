# Voice and Video Agents with n8n

Build chatbots, RAG assistants, voice agents and AI avatar/video automations with **n8n** — every lab is a runnable n8n workflow plus, where it applies, a real web front end.

| Course detail | Information |
|---|---|
| Course code | `C500` |
| Programme | Non-WSQ |
| Duration | 2 days, 15 hours (9:30am – 5:30pm, 7.5 instructional hours a day) |
| Registration | **[View course details and register](https://www.tertiarycourses.com.sg/voice-and-video-agents-with-n8n.html)** |
| Provider | Tertiary Infotech Academy Pte Ltd |

## About the course

The course teaches you to design, build, test and improve practical AI automations using n8n, Ollama, RAG, ElevenLabs, Vapi, HeyGen, LiveAvatar, Google Veo 3.1 and open-source lip-sync rendering. The emphasis is engineering judgement, not "click nodes until it works": every lab runs the agentic AI loop — **Define → Build → Observe → Evaluate → Improve → Guardrail → Document** — and produces evidence you keep: workflow exports, execution traces, call transcripts and generated media. At least 70% of the course is hands-on.

## Learning outcomes

By the end of the course, you will be able to:

- **LO1** — Analyse the strengths, limitations and feasibility of AI digital human technology within industry contexts.
- **LO2** — Evaluate the performance of AI digital human applications and analyse their effectiveness.
- **LO3** — Assess the design and improvements for AI digital human technology.

## Topics covered

| Topic | Theme | Labs | When |
|---|---|---|---|
| **1** | **Chatbot** — agents, retrieval and grounded answers | Labs 0 – 3 | Day 1 morning |
| **2** | **Voice Agent** — ElevenLabs calls your n8n tools; with Vapi your n8n workflow *is* the model | Labs 4 – 5 | Day 1 afternoon |
| **3** | **Video Agent** — lip-sync, avatars and text-to-video | Labs 6 – 10 | Day 2 |

## Labs

The same labs ship twice. Pick one tree and stay in it — the model, the credential and the webhook base all differ.

| | [`labs_local_n8n/`](labs_local_n8n/) | [`labs_remote_n8n/`](labs_remote_n8n/) |
|---|---|---|
| **n8n** | your own Docker stack ([`lab0/`](labs_local_n8n/lab0/)) | `n8n.tertiarytraining.com` (hosted) |
| **Chat model** | Ollama `gemma4:latest` | OpenAI `gpt-4.1-mini` |
| **Embeddings** | Ollama `nomic-embed-text:latest` | OpenAI `text-embedding-3-small` |
| **Needs ngrok?** | Yes, when a vendor's servers must call in | No — already public |
| **Learner guide** | [`LEARNER_GUIDE_LOCAL.md`](LEARNER_GUIDE_LOCAL.md) | [`LEARNER_GUIDE_CLOUD.md`](LEARNER_GUIDE_CLOUD.md) |

**Local** is the classroom default: free, private, nothing to bill. **Remote** is for learners who cannot run Docker.

| Lab | Title | What you build | Local | Remote |
|---|---|---|---|---|
| **0** | Set up n8n locally | Docker + n8n + Postgres + Ollama | [lab0](labs_local_n8n/lab0/) | — |
| **1** | Your First AI Agent | Chat trigger, AI Agent node and a system prompt you control | [lab1](labs_local_n8n/lab1/) | [lab1](labs_remote_n8n/lab1/) |
| **2** | RAG IT Support Chatbot | PDF → embeddings → grounded answers that admit what they do not know | [lab2](labs_local_n8n/lab2/) | [lab2](labs_remote_n8n/lab2/) |
| **3** | CX Agent with RAG (Cook & Bake Academy) | A website course advisor over a brochure knowledge base | [lab3](labs_local_n8n/lab3/) | [lab3](labs_remote_n8n/lab3/) |
| **4** | Voice Booking Agent with ElevenLabs (GG Hair Salon) | Nina books into a real Google Calendar, by voice | [lab4](labs_local_n8n/lab4/) | [lab4](labs_remote_n8n/lab4/) |
| **5** | Grounded FAQ Voice Agent with Vapi (MediRefill) | Ava, a refill assistant that refuses medical advice | [lab5](labs_local_n8n/lab5/) | [lab5](labs_remote_n8n/lab5/) |
| **6** | Lip-Sync Face-Off: MuseTalk vs HeyGen | One script and portrait through a local and a cloud renderer | [lab6](labs_local_n8n/lab6/) | [lab6](labs_remote_n8n/lab6/) |
| **7** | Avatar News Video with HeyGen (GG News Studio) | A script agent that drives an avatar presenter | [lab7](labs_local_n8n/lab7/) | [lab7](labs_remote_n8n/lab7/) |
| **7-os** | Open-Source News Avatar | The same video, rendered free on your own machine | [lab7-opensource](labs_local_n8n/lab7-opensource/) | [lab7-opensource](labs_remote_n8n/lab7-opensource/) |
| **8** | Interactive Avatar Brain (Aria, In-Browser) | A low-latency talking avatar in the browser | [lab8](labs_local_n8n/lab8/) | [lab8](labs_remote_n8n/lab8/) |
| **9** | Interactive Avatar Session (Nova, HeyGen LiveAvatar) | An embedded interactive avatar | [lab9](labs_local_n8n/lab9/) | [lab9](labs_remote_n8n/lab9/) |
| **10** | AI Video Generation with Gemini Veo 3 (Veo Studio) | Idea → shot script → 8-second cinematic clip | [lab10](labs_local_n8n/lab10/) | [lab10](labs_remote_n8n/lab10/) |

### Usage notes

- **Serve the lab web apps, never open them off the disk.** Use each lab's `start.command` (macOS) or `start.bat` (Windows). On a `file://` URL the browser blocks `fetch()` and the page fails with misleading errors.
- **Windows: unblock the ZIP before extracting** (right-click → Properties → tick *Unblock*). `git clone` avoids this.
- **A workflow will not run until it is Active.** An inactive workflow's `/webhook/…` path returns `404`. Every lab website has a *Test connection* button that names the failure.
- **API keys stay in n8n credentials or a local `.env`** — never in browser JavaScript, Markdown, screenshots or committed JSON.

## Courseware

| Document | Files |
|---|---|
| Slide deck (v2.0) | [PPTX](<courseware/Voice and Video Agents with n8n (C500)-v2.0.pptx>) · [PDF](<courseware/Voice and Video Agents with n8n (C500)-v2.0.pdf>) |
| Learner Guide | [DOCX](<courseware/LG-Voice and Video Agents with n8n (C500).docx>) · [PDF](<courseware/LG-Voice and Video Agents with n8n (C500).pdf>) · [Markdown](<courseware/LG-Voice and Video Agents with n8n (C500).md>) |
| Lesson Plan | [DOCX](<courseware/LP-Voice and Video Agents with n8n (C500).docx>) · [PDF](<courseware/LP-Voice and Video Agents with n8n (C500).pdf>) · [Markdown](<courseware/LP-Voice and Video Agents with n8n (C500).md>) |

## Distribution

This repository is the public courseware for C500: slides, Learner Guide, Lesson Plan and both lab trees. Trainer-only and source reference material is kept out of the public repository.

---

© 2026 Tertiary Infotech Academy Pte Ltd · [www.tertiarycourses.com.sg](https://www.tertiarycourses.com.sg)

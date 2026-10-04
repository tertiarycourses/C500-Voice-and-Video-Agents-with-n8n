# Lesson Plan - Voice and Video Agents with n8n

## Course profile

| | |
|---|---|
| Provider | Tertiary Infotech Academy Pte Ltd |
| Course code | C500 |
| Version | v2.0 (4 October 2026) |
| Mode | Instructor-led adult training, hands-on labs |
| Duration | 2 days, 7.5 instructional hours each (9:30am - 5:30pm) |
| Practical ratio | At least 70 percent hands-on lab time |
| Trainer | Dr Alfred Ang |

## Trainer strategy

Demonstrate each concept with one small working example, then move quickly into learner practice. For every lab, ask learners to show the **evidence** - the n8n execution trace, the generated media, the call transcript, the scorecard. Do not accept a screenshot of a finished screen as proof that the workflow is correct: a fluent output and a correct workflow are not the same thing, and telling them apart is the skill this course teaches.

## Topic map

| Session | Topic | Focus | Learning outcome | Labs |
|---|---|---|---|---|
| 1 | Topic 01 - Chatbot | Agents, retrieval and grounded answers: your first n8n AI agent, a RAG chatbot that admits what it does not know, and a customer-facing course advisor on a real website. Labs 0-3. | LO1 | Lab 0, Lab 1, Lab 2, Lab 3 |
| 2 | Topic 02 - Voice Agent | Two vendors, two architectures: ElevenLabs runs the model and calls your n8n tools; with Vapi your n8n workflow IS the model. The contrast is the lesson. Labs 4-5. | LO2 | Lab 4, Lab 5 |
| 3 | Topic 03 - Video Agent | Lip-sync, avatars and text-to-video: from a script, to a mouth that moves, to a face that talks back, to video from nothing but a sentence. Labs 6-10. | LO3 | Lab 6, Lab 7, Lab 7-os, Lab 8, Lab 9, Lab 10 |

## Daily schedule

Total taught content: 13 hours 00 minutes across 12 labs.

### Day 1

| Time | Duration | Topic / Activity | Deck | Evidence produced |
|---|---|---|---|---|
| 9:30am - 10:10am | 40 min | Lab 0 - Set Up n8n Locally | Slide 18 | A running local stack: screenshots of docker compose ps, ollama list and the passing credential test. |
| 10:10am - 10:50am | 40 min | Lab 1 - Your First AI Agent | Slide 24 | A working local agent plus a one-line note on how the system prompt changed its behaviour. |
| 10:50am - 11:45am | 55 min | Lab 2 - RAG IT Support Chatbot | Slide 30 | A RAG chatbot answering from the IT FAQ, plus one provoked refusal captured in the execution trace. |
| 11:45am - 12:40pm | 55 min | Lab 3 - CX Agent with RAG (Cook & Bake Academy) | Slide 37 | A working course-advisory chatbot on the site, with one grounded answer and one honest refusal in the trace. |
| 12:40pm - 1:10pm | 30 min | **LUNCH** | - | - |
| 1:10pm - 3:10pm | 120 min | Lab 4 - Voice Booking Agent with ElevenLabs (GG Hair Salon) | Slide 50 | A real calendar booking made by voice: the calendar event, the call transcript, and the n8n tool execution. |
| 3:10pm - 4:35pm | 85 min | Lab 5 - Grounded FAQ Voice Agent with Vapi (MediRefill) | Slide 57 | A live Vapi call transcript showing grounded answers, a hard medical refusal, and the emergency escalation. |
| 4:35pm - 5:30pm | 55 min | Concept delivery, review and evidence check - the trainer teaches the concept, workflow and quality slides for the day's labs, then learners show their executions, transcripts and scorecards | - | Trainer sign-off on the day's evidence |

**Day 1 instructional time: 7h 30m** (9:30am-5:30pm, less a 30-minute lunch).

### Day 2

| Time | Duration | Topic / Activity | Deck | Evidence produced |
|---|---|---|---|---|
| 9:30am - 10:45am | 75 min | Lab 6 - Lip-Sync Face-Off: MuseTalk vs HeyGen | Slide 68 | Two rendered clips of one script, a scored comparison, and a one-line recommendation per engine. |
| 10:45am - 11:45am | 60 min | Lab 7 - Avatar News Video with HeyGen (GG News Studio) | Slide 75 | Your own news broadcast, played to the class, plus quality-review notes on the script and the render. |
| 11:45am - 12:45pm | 60 min | Lab 7-os - Open-Source News Avatar - Free and Local | Slide 81 | A locally rendered news video and a written HeyGen-versus-local comparison. |
| 12:45pm - 1:15pm | 30 min | **LUNCH** | - | - |
| 1:15pm - 2:15pm | 60 min | Lab 8 - Interactive Avatar Brain (Aria, In-Browser) | Slide 87 | A conversation with Aria, the latency-panel screenshot, and one prompt improvement you made and re-tested. |
| 2:15pm - 3:15pm | 60 min | Lab 9 - Interactive Avatar Session (Nova, HeyGen LiveAvatar) | Slide 93 | A working Nova session plus the two-column scorecard comparing her against the browser-rendered avatar. |
| 3:15pm - 4:30pm | 75 min | Lab 10 - AI Video Generation with Gemini Veo 3 (Veo Studio) | Slide 99 | Your own Veo clip presented to the class, the shot prompt that produced it, and a note on what changed between two prompt versions. |
| 4:30pm - 5:30pm | 60 min | Concept delivery, review, evidence check and course feedback - the trainer teaches the concept, workflow and quality slides for the day's labs, then learners show their executions, transcripts and scorecards | - | Trainer sign-off on the day's evidence |

**Day 2 instructional time: 7h 30m** (9:30am-5:30pm, less a 30-minute lunch).


## Evidence the trainer collects

- Workflow exports and n8n execution traces for each lab.
- The provoked failures: the RAG refusal (Lab 2), the course that does not exist (Lab 3), Ava's medical refusals (Lab 5).
- The Google Calendar booking created by voice, with its call transcript (Lab 4).
- The lip-sync comparison scorecard: MuseTalk vs HeyGen on one script (Lab 6).
- Generated media: the news avatar videos (Labs 7 and 7-os), the Aria latency screenshot (Lab 8), the Nova session scorecard (Lab 9), the Veo clip and its shot prompt (Lab 10).

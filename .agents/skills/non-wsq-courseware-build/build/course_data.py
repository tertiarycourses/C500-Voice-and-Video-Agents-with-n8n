"""Single source of truth for Voice and Video Agents with n8n (C500)."""

TITLE = "Voice and Video Agents with n8n (C500)"
SHORT_TITLE = "Voice and Video Agents with n8n (C500)"
COURSE_CODE = "C500"
VERSION = "v1.0"
VERSION_DATE = "11 August 2026"
ORG = "Tertiary Infotech Academy Pte Ltd"
UEN = "UEN: 201200696W"
TRAINER = "Tertiary Infotech Academy Training Team"
TRAINER_CERT = "Practitioner in workflow automation, conversational AI and synthetic media production."
TRAINER_DELIVERS = "Applied AI, agent automation and no-code workflow courses."
DAYS = 1
DAY_MINUTES = 480
DAILY_TIMING = "9:00 am - 6:00 pm (1-hour lunch; tea breaks within scheduled time)"
MODE = "Instructor-led, concept-first demonstrations and connected hands-on labs"
COURSE_URL = "https://www.tertiarycourses.com.sg/voice-and-video-agents-with-n8n.html"
REPO_URL = "https://github.com/tertiarycourses/C500-Voice-and-Video-Agents-with-n8n"
DARK_THEME = False

LEARNING_OUTCOMES = [
    "LO1: Explain the listen-think-talk architecture of a voice agent, select suitable business use cases, and design the n8n workflow and channel boundary.",
    "LO2: Build and verify an n8n voice agent that transcribes audio with Whisper, reasons with an AI Agent, speaks with ElevenLabs, and operates through browser and chat channels.",
    "LO3: Explain avatar-video architecture and build an n8n workflow that turns a governed brief into a talking-head video through an asynchronous video API.",
    "LO4: Automate a monitored video-production and distribution pipeline with approval, retry, accessibility, privacy, cost and human-handoff controls.",
]

LO_TITLES = [
    "Voice Architecture",
    "Working Voice Agent",
    "Avatar Video Agent",
    "Governed Automation",
]

TOPICS = [
    dict(
        num=1,
        code="01",
        title="Voice Agent",
        subtitle="AI voice agents and n8n | webhooks and AI Agent nodes | Whisper and ElevenLabs | browser, chat and phone patterns | service use cases",
        concepts=[
            "A voice agent is a conversational system that accepts speech, derives text and intent, chooses a bounded response, then renders speech; audio alone does not make a workflow agentic.",
            "n8n orchestrates triggers, binary audio, model calls, credentials, branches, retries and channel delivery while external models perform transcription, reasoning and speech synthesis.",
            "Speech-to-text converts an audio signal into a transcript; the AI Agent interprets that transcript against role, context and policy rather than treating it as an instruction with unlimited authority.",
            "Text-to-speech converts approved response text into audio; voice identity, pronunciation, language, pace and output format are production parameters.",
            "Browser, messaging and telephone channels expose different audio formats, session identifiers, time limits and response contracts, so the conversation core should be separated from channel adapters.",
            "Perceived quality depends on the full latency budget: capture, upload, transcription, reasoning, synthesis and delivery all contribute to the pause a caller experiences.",
            "Conversation state needs an explicit key, bounded memory and expiry; channel identifiers are useful routing data but should not silently become long-term personal profiles.",
            "A safe voice agent discloses its automated nature, minimises recordings and transcripts, validates callers before sensitive actions, logs decisions, and hands off when confidence or authority is insufficient.",
        ],
        concept_sections=[
            dict(
                title="Voice Agent or Voice Automation?",
                kicker="USE-CASE FIT",
                paragraphs=[
                    "A recorder, transcription job or fixed menu may use speech without being an agent. A voice agent interprets a conversational goal, chooses among permitted actions and continues until it can answer, clarify or hand off. Use the simplest pattern that satisfies the service need.",
                    "HarbourStay begins with frequently asked guest questions because the answers are bounded and a wrong reply is reversible. Payments, identity changes, emergency advice and contractual commitments stay with authorised staff even if the same voice interface receives the request.",
                ],
                visual=[
                    ("Transcribe", "Speech becomes text; no decision is made."),
                    ("Route", "A known intent selects a fixed workflow branch."),
                    ("Agent", "A bounded model chooses a response or tool."),
                    ("Human", "Consequential or uncertain requests leave automation."),
                ],
            ),
            dict(
                title="The Listen-Think-Talk Loop",
                kicker="CORE ARCHITECTURE",
                paragraphs=[
                    "Listen captures audio, validates the file and transcribes it. Think applies the role, approved knowledge, conversation context and available tools. Talk converts only the approved response into audio and returns it through the originating channel.",
                    "Verification closes the loop. The workflow checks that every stage returned usable evidence, that no unapproved action occurred, and that the final audio corresponds to the response text. A failure at one stage must not be disguised by a fluent later stage.",
                ],
                visual=[
                    ("Listen", "Capture -> validate -> transcribe."),
                    ("Think", "Interpret -> retrieve -> decide."),
                    ("Talk", "Approve text -> synthesise -> deliver."),
                    ("Verify", "Trace stages, evidence and fallback."),
                ],
            ),
            dict(
                title="n8n as the Conversation Orchestrator",
                kicker="WORKFLOW MAP",
                paragraphs=[
                    "The Webhook or Telegram Trigger starts a run. Core nodes normalise channel-specific fields, provider nodes or HTTP Request nodes call the models, the AI Agent applies the role, and a response node honours the channel contract. Credentials remain in n8n credential storage.",
                    "Keep provider calls in named subflows or clearly labelled nodes. This makes models replaceable, errors observable and usage measurable. The workflow is responsible for routing and control even when the language model supplies the wording.",
                ],
                visual=[
                    ("Trigger", "Receive audio and a stable conversation key."),
                    ("Normalise", "Produce one transcript request schema."),
                    ("Conversation Core", "Apply role, context and response policy."),
                    ("Adapter", "Return browser audio, chat audio or call markup."),
                ],
            ),
            dict(
                title="Audio Transport and Binary Data",
                kicker="MEDIA CONTRACT",
                paragraphs=[
                    "Audio reaches n8n as binary data, a downloadable file identifier or a provider URL. The workflow must preserve the binary field name, MIME type and filename expected by the transcription call. A JSON body that merely names a local file cannot carry that file across the network.",
                    "Browser MediaRecorder commonly produces WebM audio, Telegram voice notes use OGG/Opus, and telephone platforms may use streamed or provider-hosted audio. Validate size and type early, then convert only when the chosen provider requires it.",
                ],
                visual=[
                    ("Browser", "Multipart upload from MediaRecorder."),
                    ("Telegram", "File ID -> download -> binary property."),
                    ("Phone", "Call event plus media stream or recording URL."),
                    ("Provider", "Accepted format, limit and response schema."),
                ],
            ),
            dict(
                title="Whisper Transcription Is Evidence, Not Intent",
                kicker="SPEECH TO TEXT",
                paragraphs=[
                    "The transcription model estimates words from audio. Noise, accents, product names and code-switching can change the transcript. Preserve the observed transcript and language metadata so later failures can be traced to listening rather than reasoning.",
                    "Do not let a transcript directly trigger a high-impact action. Normalise the text, detect empty or implausible results and ask the speaker to repeat when needed. Domain vocabulary can be supplied as context, but the agent still needs confirmation for names, dates and quantities.",
                ],
                visual=[
                    ("Audio Check", "Type, size, duration and signal are usable."),
                    ("Transcribe", "Whisper returns text and optional metadata."),
                    ("Normalise", "Trim, label language and keep provenance."),
                    ("Clarify", "Repeat critical facts instead of guessing."),
                ],
            ),
            dict(
                title="AI Agent Role and Response Contract",
                kicker="THINKING BOUNDARY",
                paragraphs=[
                    "A production system message names the organisation, authorised topics, style, sources, forbidden actions and escalation route. It also defines a machine-readable response contract so downstream nodes can distinguish an answer from a handoff or clarification.",
                    "Source content and caller speech are untrusted data. They may describe instructions but cannot expand tools, reveal hidden prompts or waive policy. The AI Agent should state limitations and return a safe handoff when the required evidence is not available.",
                ],
                visual=[
                    ("Role", "Who the agent represents and serves."),
                    ("Scope", "Topics and actions it may handle."),
                    ("Response", "Answer, clarify or handoff with reason."),
                    ("Evidence", "Source, timestamp and uncertainty retained."),
                ],
            ),
            dict(
                title="ElevenLabs Speech Synthesis",
                kicker="TEXT TO SPEECH",
                paragraphs=[
                    "The text-to-speech request combines approved text, a voice identifier, a model and output settings. The response is binary audio; n8n must preserve it through to the browser or messaging node. Synthesising before policy checks risks giving unsafe text a persuasive voice.",
                    "Choose a voice that is intelligible for the language and context. Test names, abbreviations, numbers and URLs. Short sentences and spoken punctuation improve comprehension, while excessive expressiveness can be inappropriate for service or safety messages.",
                ],
                visual=[
                    ("Input", "Approved response text only."),
                    ("Voice", "Authorised voice ID and language fit."),
                    ("Model", "Quality, latency and cost choice."),
                    ("Output", "Audio format suited to the channel."),
                ],
            ),
            dict(
                title="Channel Adapters: Browser, Chat and Phone",
                kicker="ONE CORE, MANY CHANNELS",
                paragraphs=[
                    "A browser can wait for one HTTP response and play returned audio. A chat platform delivers separate events and files, so the workflow replies to a chat identifier. A telephone platform adds call lifecycle events, strict response timing and telephony-specific markup or streaming.",
                    "Keep the conversation core independent of these differences. Each adapter maps its inbound event to transcript, session and caller context, then maps answer, clarification or handoff back to the channel. This avoids duplicating policy across three workflows.",
                ],
                visual=[
                    ("Browser", "Webhook in; audio response out."),
                    ("Chat", "Message event; file download; reply to chat."),
                    ("Phone", "Call event; low-latency turn or callback."),
                    ("Core", "Same role, policy and knowledge contract."),
                ],
            ),
            dict(
                title="Latency Budget and Conversation Turn Design",
                kicker="USER EXPERIENCE",
                paragraphs=[
                    "Silence feels longer in speech than in a web form. Measure capture upload, transcription, reasoning, synthesis and delivery separately. Faster models, shorter prompts and shorter answers help only when that stage is the real bottleneck.",
                    "For slow paths, acknowledge the request or move to an asynchronous channel rather than leaving the caller in silence. Streaming can reduce perceived delay, but it also makes moderation and interruption handling harder, so use it deliberately.",
                ],
                visual=[
                    ("Capture", "End-of-speech detection and upload."),
                    ("Listen", "Transcription provider time."),
                    ("Think", "Context load, tools and model generation."),
                    ("Talk", "Synthesis plus channel delivery."),
                ],
            ),
            dict(
                title="Conversation State, Memory and Idempotency",
                kicker="CONTROL CONTINUITY",
                paragraphs=[
                    "A session key binds related turns. Store only the context needed for continuity, apply an expiry and separate durable customer records from transient conversation memory. A channel username or chat ID is not proof of identity for protected information.",
                    "Events can be retried. Use provider event IDs or a derived idempotency key to prevent duplicate bookings, messages or usage charges. The agent should be able to repeat an informational answer without repeating a side effect.",
                ],
                visual=[
                    ("Session", "Stable key for related turns."),
                    ("Memory", "Minimum context with retention limit."),
                    ("Identity", "Separate verification before protected actions."),
                    ("Idempotency", "One side effect per event or request."),
                ],
            ),
            dict(
                title="Failures, Fallbacks and Human Handoff",
                kicker="SERVICE RECOVERY",
                paragraphs=[
                    "Transcription can be empty, models can time out, speech synthesis can fail and channels can reject a file. Classify each error, retry only transient failures and preserve a plain-text fallback where the channel permits it.",
                    "A useful handoff includes the caller's stated goal, transcript, steps already attempted, relevant evidence and consented contact route. It must not expose credentials or hidden instructions. The human owner needs enough context to continue without forcing the customer to start again.",
                ],
                visual=[
                    ("Retry", "Bounded backoff for transient provider errors."),
                    ("Clarify", "Ask again when speech or intent is unclear."),
                    ("Fallback", "Return text or a safe service message."),
                    ("Handoff", "Transfer context to a named human queue."),
                ],
            ),
            dict(
                title="Privacy, Consent and Voice Safety",
                kicker="TRUST BOUNDARY",
                paragraphs=[
                    "Tell people they are interacting with an automated system and whether audio or transcripts are retained. Collect only what the service needs, protect credentials in n8n and remove recordings according to a documented retention rule.",
                    "Never clone a person's voice without documented authority. Confirm identity before exposing booking or account data, block sensitive data from logs, and maintain an immediate route to a person for emergencies, complaints and vulnerable users.",
                ],
                visual=[
                    ("Disclose", "Automated identity and recording notice."),
                    ("Minimise", "Least audio, transcript and profile data."),
                    ("Authorise", "Approved voice, data and tool permissions."),
                    ("Escalate", "Human route for consequential requests."),
                ],
            ),
            dict(
                title="Tool Authority and Transaction Boundaries",
                kicker="SAFE ACTION DESIGN",
                paragraphs=[
                    "Conversation and action are different privileges. An agent may explain a policy without being allowed to change a booking, charge a card or reveal an account record. Give each tool one narrow purpose, validated inputs and a named owner.",
                    "Before an irreversible or sensitive action, verify identity outside the model, restate the proposed change and require explicit confirmation. Record the tool input and result so fluent speech never becomes the only evidence of a transaction.",
                ],
                visual=[
                    ("Inform", "Answer from approved service facts."),
                    ("Prepare", "Draft an action without committing it."),
                    ("Confirm", "Verify identity and explicit intent."),
                    ("Execute", "Use one authorised tool and log its result."),
                ],
            ),
            dict(
                title="Voice Prompt Injection and Untrusted Speech",
                kicker="INPUT DEFENCE",
                paragraphs=[
                    "A caller can speak instructions such as 'ignore your rules' or ask for hidden configuration. Treat the transcript as user data, not as a system message. The role, policy and tool permissions remain outside the caller-controlled content.",
                    "Retrieved pages and transcripts can contain the same attack. Separate quoted evidence from instructions, allow-list tools and route attempts to reveal secrets or expand authority to a safe refusal or human review.",
                ],
                visual=[
                    ("Separate", "System policy is not caller-controlled text."),
                    ("Allow-list", "Only named tools and actions are reachable."),
                    ("Validate", "Check arguments before every side effect."),
                    ("Escalate", "Refuse or hand off suspicious requests."),
                ],
            ),
            dict(
                title="Language, Pronunciation and Inclusive Speech",
                kicker="VOICE QUALITY",
                paragraphs=[
                    "Language detection, accent and code-switching can change both transcription and synthesis. Supply domain terms where supported, confirm critical names or numbers, and test the same service facts with representative speakers rather than assuming one clean recording.",
                    "Write for listening: short sentences, expanded abbreviations and natural pauses. Provide a text alternative when speech is hard to hear, and never use vocal style to imply a human identity or certainty the system does not have.",
                ],
                visual=[
                    ("Detect", "Observe language; do not guess silently."),
                    ("Confirm", "Repeat names, dates and quantities."),
                    ("Pronounce", "Test domain terms and abbreviations."),
                    ("Include", "Offer text and human alternatives."),
                ],
            ),
            dict(
                title="Voice-Agent Observability",
                kicker="OPERATING METRICS",
                paragraphs=[
                    "A successful HTTP response does not prove a useful conversation. Track transcription success, route choice, handoff rate, stage latency, provider errors and the share of answers grounded in approved facts. Keep request IDs consistent across stages.",
                    "Review sampled failures with redacted evidence. Rising clarification rates may indicate noisy audio or missing vocabulary; rising handoffs may indicate a knowledge gap; slow synthesis may call for a different voice model rather than a larger language model.",
                ],
                visual=[
                    ("Quality", "Grounded answer and clarification rates."),
                    ("Safety", "Handoffs, refusals and blocked actions."),
                    ("Latency", "Listen, think, talk and delivery time."),
                    ("Cost", "Usage per completed useful turn."),
                ],
            ),
            dict(
                title="Phone Deployment Decision Record",
                kicker="CHANNEL READINESS",
                paragraphs=[
                    "A telephone pilot needs more than replacing the browser webhook. Record the provider event schema, media transport, call identifier, response deadline, disclosure, verified transfer route and behaviour when the caller interrupts or disconnects.",
                    "Name the regions, hours and request types permitted for the pilot. Keep payments, emergency advice and protected account changes outside scope until identity, recording consent, monitoring and rollback have been separately approved.",
                ],
                visual=[
                    ("Contract", "Events, media and response deadline."),
                    ("Identity", "Verified factor before protected data."),
                    ("Transfer", "Named queue with failure behaviour."),
                    ("Rollback", "Disable route and preserve evidence."),
                ],
            ),
            dict(
                title="Worked Trace: HarbourStay Late Check-In",
                kicker="END-TO-END EXAMPLE",
                paragraphs=[
                    "A guest asks, 'Can I arrive after midnight?' The browser adapter uploads one WebM recording. Whisper returns the observed transcript. The concierge role answers from the supplied service facts and does not claim to change the booking. ElevenLabs renders the approved response.",
                    "The verification record contains the request ID, audio type, transcript, response text, route, provider status and latency per stage. If the guest asks to change a named reservation, the agent requests a verified handoff instead of treating the spoken name as sufficient identity.",
                ],
                visual=[
                    ("Request", "Audio plus request ID; no credentials in payload."),
                    ("Transcript", "Observed question retained for traceability."),
                    ("Decision", "Information answer; no booking side effect."),
                    ("Delivery", "MP3 returned; trace proves each stage."),
                ],
            ),
        ],
        recap=[
            "You can now: LO1: Explain the listen-think-talk architecture, select bounded voice use cases, and define channel, tool and human-handoff boundaries.",
            "You can now: LO2: Build and verify a Whisper-to-AI-Agent-to-ElevenLabs workflow for browser and Telegram voice channels.",
        ],
    ),
    dict(
        num=2,
        code="02",
        title="Video Agent",
        subtitle="AI video agents and digital avatars | talking-head video APIs | asynchronous n8n production | marketing, training and service | governed distribution",
        concepts=[
            "A video agent turns an objective and approved source material into a planned, generated, checked and distributed media artifact; generation is one stage of the agent workflow.",
            "A talking-head request combines script, avatar or talking-photo identity, voice, language, dimensions and optional background or captions into a provider-specific job schema.",
            "Video generation is asynchronous: a create request returns a job identifier, while later status checks return processing, completed or failed state and eventually a media URL.",
            "The script is the highest-leverage control: it names audience, objective, claim sources, spoken length, call to action and forbidden claims before an avatar renders it persuasively.",
            "Consent and provenance must cover the avatar image, voice, music, logos and factual source material; synthetic media should be disclosed when context could mislead viewers.",
            "n8n makes the pipeline observable through request IDs, polling limits, error branches, usage logs, approvals and distribution adapters rather than an opaque sequence of API calls.",
            "Distribution is a separate decision from generation. A completed file can enter an approval queue, asset library, Telegram channel or social publishing adapter without granting the generator unlimited publishing rights.",
            "Video quality includes factual accuracy, pronunciation, captions, visual safety, aspect ratio, accessibility, rendering latency and cost per accepted asset, not just visual realism.",
        ],
        concept_sections=[
            dict(
                title="Video Generator or Video Agent?",
                kicker="AGENTIC PIPELINE",
                paragraphs=[
                    "A generator turns a supplied script into media. A video agent starts from a business objective, prepares a bounded script, selects approved assets, submits a render, observes job state, applies release checks and routes the result. The surrounding decisions make the workflow agentic.",
                    "Use a fixed template when the message barely changes. Use an agent when the brief varies and the script needs bounded reasoning. Keep a person in the release path when the content contains claims, named individuals, regulated advice or broad public reach.",
                ],
                visual=[
                    ("Template", "Known text and fixed media slots."),
                    ("Generator", "Script and assets become a video."),
                    ("Agent", "Plans, renders, observes and routes."),
                    ("Publisher", "Separate authority releases the asset."),
                ],
            ),
            dict(
                title="Talking-Head Video Anatomy",
                kicker="MEDIA BUILDING BLOCKS",
                paragraphs=[
                    "The provider needs a visual identity, a voice or audio source, spoken text, scene settings and output dimensions. Some APIs use stock avatar IDs; others animate a talking photo. IDs are configuration values and should be validated before a production run.",
                    "The same script can produce very different results with a new avatar, voice, pace or aspect ratio. Store these choices as an approved campaign profile rather than scattering them across workflow expressions.",
                ],
                visual=[
                    ("Script", "Approved spoken words and pronunciation cues."),
                    ("Avatar", "Authorised visual identity or talking photo."),
                    ("Voice", "Authorised voice ID, language and pace."),
                    ("Canvas", "Aspect ratio, background and captions."),
                ],
            ),
            dict(
                title="HeyGen Asynchronous Job Lifecycle",
                kicker="CREATE -> OBSERVE -> RESOLVE",
                paragraphs=[
                    "The create-video request is accepted before rendering finishes and returns a video identifier. The workflow stores that identifier, waits, asks the status endpoint and branches on completed, failed or still-processing state. A successful HTTP response is not proof that a video exists.",
                    "Set a maximum number of checks and an overall deadline. Preserve provider error details, and avoid creating a second render merely because a status call was slow. The original request ID and video ID are the evidence needed for safe recovery.",
                ],
                visual=[
                    ("Create", "Validate brief and submit one render job."),
                    ("Store", "Keep request ID, video ID and submitted settings."),
                    ("Poll", "Wait, check state and count attempts."),
                    ("Resolve", "Completed URL, failure record or timeout queue."),
                ],
            ),
            dict(
                title="Script Contract: Brief to Spoken Copy",
                kicker="CONTENT CONTROL",
                paragraphs=[
                    "The script prompt names audience, outcome, source facts, spoken duration, tone, call to action and exclusions. Require a structured result with title, spoken script, caption and claim list so later checks do not need to infer what the model intended.",
                    "Spoken copy needs short sentences, explicit pronunciation and no invisible formatting. Estimate duration from word count, then enforce a maximum. A beautiful render should be rejected if the script exceeds the time box or introduces an unsupported claim.",
                ],
                visual=[
                    ("Audience", "Who watches and what they already know."),
                    ("Outcome", "One useful action after watching."),
                    ("Sources", "Approved facts and offer wording."),
                    ("Constraints", "Length, tone, claims and disclosure."),
                ],
            ),
            dict(
                title="Avatar and Voice Consent",
                kicker="IDENTITY RIGHTS",
                paragraphs=[
                    "Stock provider assets come with platform terms; custom likenesses and voices require documented authority from the represented person and the organisation. Consent should cover intended channels, territories, duration and withdrawal handling.",
                    "Do not use an avatar to imply that a real person personally delivered or endorsed content when they did not. Maintain asset provenance and a reviewable campaign profile so a future workflow run cannot silently switch identities.",
                ],
                visual=[
                    ("Owner", "Who controls the image, voice and brand assets."),
                    ("Purpose", "Permitted messages and audience."),
                    ("Term", "Duration, channels and withdrawal process."),
                    ("Disclosure", "When viewers must know media is synthetic."),
                ],
            ),
            dict(
                title="Campaign Profile and Asset Configuration",
                kicker="REUSABLE SETTINGS",
                paragraphs=[
                    "A campaign profile centralises avatar ID, voice ID, language, aspect ratio, logo, background, disclosure, destination and owner. The workflow reads this approved configuration instead of asking a language model to invent provider IDs.",
                    "Version the profile and validate it before submission. If a provider asset is removed, fail with a configuration message and route to the owner. Do not fall back to an arbitrary face or voice merely to complete the run.",
                ],
                visual=[
                    ("Identity", "Avatar and voice IDs with provenance."),
                    ("Format", "Dimensions, background, captions and language."),
                    ("Release", "Owner, destination and disclosure rule."),
                    ("Version", "Effective date and change reason."),
                ],
            ),
            dict(
                title="Polling, Timeouts and Idempotent Recovery",
                kicker="ASYNC RELIABILITY",
                paragraphs=[
                    "A Wait node spaces provider checks; an IF or Switch node interprets state; a loop counter prevents an endless run. Record the next permitted check time if the API communicates a rate limit, and route an exhausted deadline to an operator.",
                    "A retry of status is safe; a retry of creation may incur a second charge and duplicate asset. Create once per approved request key. Recovery resumes observation of the known video ID unless evidence proves the provider never accepted the original request.",
                ],
                visual=[
                    ("Wait", "Respect render time and provider rate limits."),
                    ("Check", "Completed, failed or processing state."),
                    ("Limit", "Maximum attempts and elapsed deadline."),
                    ("Resume", "Continue known job; do not duplicate creation."),
                ],
            ),
            dict(
                title="End-to-End Production Pipeline",
                kicker="ORCHESTRATION MAP",
                paragraphs=[
                    "The production pipeline separates intake, script preparation, approval, render, quality checks, storage and delivery. Each stage has an owner and an observable artifact. This makes a failed caption check recoverable without regenerating the script and avatar unnecessarily.",
                    "Use sub-workflows when the same rendering or distribution logic serves multiple campaigns. Pass a compact contract rather than the entire trigger payload, and return the video ID, final URL, checks and failure details.",
                ],
                visual=[
                    ("Prepare", "Brief -> facts -> structured script."),
                    ("Approve", "Claims, identity and destination checked."),
                    ("Render", "Create once and observe job state."),
                    ("Release", "Store, caption, distribute and log."),
                ],
            ),
            dict(
                title="Distribution Adapters and Release Authority",
                kicker="PUBLISHING BOUNDARY",
                paragraphs=[
                    "A completed provider URL is a candidate asset, not automatic permission to publish. The distribution layer verifies approval state, visibility, caption, destination identity and platform limits before upload or posting.",
                    "The C500 pipeline stores the asset record and demonstrates a Telegram channel adapter. The same contract can feed a content management or social API, but each adapter needs its own credentials, rate limits, moderation rules and rollback procedure.",
                ],
                visual=[
                    ("Asset Library", "Stable record, provenance and retention."),
                    ("Approval Queue", "Named reviewer and release decision."),
                    ("Channel", "Caption, media limits and target identity."),
                    ("Rollback", "Unpublish, correct and notify owner."),
                ],
            ),
            dict(
                title="Observability, Cost and Capacity",
                kicker="OPERATING METRICS",
                paragraphs=[
                    "Track accepted requests, script approvals, create calls, completed renders, failed renders, timeouts, published assets and human interventions. Store timestamps for each stage so bottlenecks are visible rather than blamed on the final provider.",
                    "Cost per accepted video is more useful than cost per API call because rejected or duplicate renders consume budget without delivering value. Limit duration, resolution, retries and campaign frequency, and alert before a monthly cap is exhausted.",
                ],
                visual=[
                    ("Reliability", "Completed renders / accepted requests."),
                    ("Latency", "Median and tail time by stage."),
                    ("Quality", "Accepted assets / completed renders."),
                    ("Cost", "Provider spend / accepted assets."),
                ],
            ),
            dict(
                title="Accessibility and Release Quality",
                kicker="VIEWER EXPERIENCE",
                paragraphs=[
                    "Captions support silent viewing and people who cannot rely on audio. Review reading speed, colour contrast, text placement and mobile aspect ratio. Supply a transcript or equivalent text alongside important training and service content.",
                    "Quality review compares the rendered words with the approved script, checks pronunciation and verifies that the image, voice, background and branding match the campaign profile. Accessibility and factual checks are release criteria, not optional polish.",
                ],
                visual=[
                    ("Words", "Rendered speech matches approved script."),
                    ("Captions", "Accurate, readable and time-aligned."),
                    ("Visual", "Safe framing, contrast and correct identity."),
                    ("Alternative", "Transcript or text equivalent available."),
                ],
            ),
            dict(
                title="Video Safety and Content Provenance",
                kicker="TRUSTED MEDIA",
                paragraphs=[
                    "Save the source brief, facts, script version, asset profile, provider job ID, reviewer and distribution target. This provenance supports corrections and prevents a final URL from becoming an untraceable media object.",
                    "Block requests that impersonate people, fabricate testimonials, hide material disclosures or use unlicensed assets. External text can inform a script only after source authority is checked; it cannot command the workflow to skip review or change the destination.",
                ],
                visual=[
                    ("Source", "Approved facts and content owner."),
                    ("Transform", "Prompt, script and profile versions."),
                    ("Render", "Provider, video ID and check results."),
                    ("Release", "Reviewer, destination and published time."),
                ],
            ),
            dict(
                title="Moderation Before and After Rendering",
                kicker="TWO CHECKPOINTS",
                paragraphs=[
                    "Pre-render review checks the brief, claims, script, avatar, voice and destination before cost is incurred. Post-render review checks what viewers will actually receive: spoken words, captions, framing, visual artefacts and the final disclosure.",
                    "A pass at one checkpoint cannot replace the other. Provider rendering can introduce pronunciation or caption errors, while a polished final video can still be based on an unapproved claim or identity.",
                ],
                visual=[
                    ("Brief", "Authority, source facts and audience."),
                    ("Script", "Claims, length and disclosure approved."),
                    ("Render", "Authorised identity and one job ID."),
                    ("Asset", "Words, captions, framing and destination."),
                ],
            ),
            dict(
                title="Scene, Caption and Aspect-Ratio Design",
                kicker="LAYOUT CONTRACT",
                paragraphs=[
                    "A 16:9 training screen and a 9:16 mobile story have different safe areas. Keep faces, logos and captions within the target frame; limit on-screen text; and choose a background that preserves contrast without implying a location or endorsement that is not real.",
                    "Captions need readable line lengths and accurate timing. Treat dimensions, caption setting, background and safe-area rules as a versioned campaign profile so repeatable output does not depend on manual memory.",
                ],
                visual=[
                    ("Frame", "Choose 16:9, 9:16 or 1:1 deliberately."),
                    ("Safe Area", "Keep face, logo and text visible."),
                    ("Captions", "Readable lines with accurate timing."),
                    ("Profile", "Version dimensions and layout settings."),
                ],
            ),
            dict(
                title="Provider Portability and Stable Contracts",
                kicker="REPLACEABLE SERVICES",
                paragraphs=[
                    "Video providers name avatars, voices, statuses and output fields differently. Keep one internal render request and result schema, then isolate provider-specific translation in named nodes or subflows.",
                    "A stable internal contract makes migration and testing easier. It also lets a failure branch describe one error class even when the provider changes its raw response, without hiding the original status needed for diagnosis.",
                ],
                visual=[
                    ("Request", "Script, profile and idempotency key."),
                    ("Adapter", "Translate to provider job schema."),
                    ("Status", "Map processing, completed and failed."),
                    ("Evidence", "Keep raw job ID and normalised result."),
                ],
            ),
            dict(
                title="Content Change Control",
                kicker="APPROVED SNAPSHOT",
                paragraphs=[
                    "Approval must bind to the exact script, profile and destination reviewed by a person. Hash the script, version the campaign profile and store the approved destination; do not regenerate or silently substitute any of them after approval.",
                    "A later wording change creates a new snapshot and needs a new approval. The release workflow recomputes the hash and compares every value before rendering or publishing, making review evidence technically enforceable rather than ceremonial.",
                ],
                visual=[
                    ("Snapshot", "Exact script and release metadata."),
                    ("Hash", "Detect any wording change."),
                    ("Version", "Bind avatar, voice and layout."),
                    ("Destination", "Publish only to reviewed channel."),
                ],
            ),
            dict(
                title="Rollback and Media Incident Response",
                kicker="AFTER RELEASE",
                paragraphs=[
                    "Rollback removes or disables the distributed asset while preserving the run record, source snapshot and provider job evidence. Deleting the audit trail makes it harder to understand the incident or prevent recurrence.",
                    "The runbook names an owner, reviewer, channel administrator and escalation contact. It defines how to stop the schedule, remove the private post, rotate compromised credentials and communicate a correction without starting another render blindly.",
                ],
                visual=[
                    ("Stop", "Disable schedule and new releases."),
                    ("Contain", "Remove or restrict the published asset."),
                    ("Preserve", "Keep snapshot, job and decision evidence."),
                    ("Correct", "Approve a new version before republishing."),
                ],
            ),
            dict(
                title="Worked Trace: HarbourStay Welcome Video",
                kicker="END-TO-END EXAMPLE",
                paragraphs=[
                    "Marketing submits a welcome brief with three approved facts and a forty-five-second limit. The script node returns structured copy with no price claim. A reviewer approves the avatar, voice and destination. The create call returns one video ID and the workflow polls until completion.",
                    "Release checks compare the spoken message with the approved script, confirm captions and disclosure, then save the provider URL and send it to the training Telegram channel. The run record proves who approved the content and which job produced the asset.",
                ],
                visual=[
                    ("Brief", "Audience, facts, CTA and duration."),
                    ("Approval", "Script, identity and destination."),
                    ("Render", "One video ID; bounded polling."),
                    ("Release", "Checks, channel delivery and provenance."),
                ],
            ),
        ],
        recap=[
            "You can now: LO3: Explain avatar-video architecture and build a governed brief-to-script-to-asynchronous-render workflow.",
            "You can now: LO4: Operate an approved, idempotent video pipeline with release checks, private distribution, monitoring and rollback.",
        ],
    ),
]

DAY_THEMES = {
    1: "Build and govern voice and avatar-video agents with n8n",
}


def SCHEDULE(lab_titles):
    return {
        1: (DAY_THEMES[1], [
            ("9:00", "9:20", 20, "admin", "Welcome, outcomes, resources and responsible-use ground rules"),
            ("9:20", "10:05", 45, "topic", "Topic 1 - Voice Agent: use-case fit, listen-think-talk architecture and n8n orchestration"),
            ("10:05", "10:25", 20, "topic", "Audio transport, Whisper transcription and ElevenLabs synthesis demonstration"),
            ("10:25", "10:40", 15, "break", "Tea break"),
            ("10:40", "11:35", 55, "lab", "Hands-on: " + lab_titles([1])),
            ("11:35", "12:15", 40, "topic", "Channel adapters, latency, state, privacy and human handoff"),
            ("12:15", "13:00", 45, "lab", "Hands-on: " + lab_titles([2])),
            ("13:00", "14:00", 60, "lunch", "Lunch break"),
            ("14:00", "14:15", 15, "recap", "Voice-agent trace review and transition to video"),
            ("14:15", "15:00", 45, "topic", "Topic 2 - Video Agent: avatar anatomy, script contracts and asynchronous APIs"),
            ("15:00", "15:30", 30, "topic", "Polling, consent, accessibility, quality and cost controls"),
            ("15:30", "15:45", 15, "break", "Tea break"),
            ("15:45", "16:40", 55, "lab", "Hands-on: " + lab_titles([3])),
            ("16:40", "17:00", 20, "topic", "End-to-end production, approval and distribution patterns"),
            ("17:00", "17:50", 50, "lab", "Hands-on: " + lab_titles([4])),
            ("17:50", "18:00", 10, "recap", "Course recap, implementation checklist and next steps"),
        ]),
    }


COURSE_OVERVIEW = dict(
    section_title="Voice and Video Agent Fundamentals",
    concepts_title="Four Ideas That Anchor the Course",
    concepts=[
        ("Agent", "A bounded workflow that interprets an objective, chooses permitted actions, observes results and verifies completion."),
        ("Media", "Audio and video are typed binary artifacts with format, identity, rights, size and delivery requirements."),
        ("Orchestration", "n8n controls triggers, credentials, branching, retries, asynchronous jobs, evidence and channel adapters."),
        ("Release", "Generation never implies permission to act, impersonate or publish; authority remains explicit."),
    ],
    framework_title="The Shared Agent Lifecycle",
    framework=[
        ("Receive", "Accept an event, validate its source and assign a request key."),
        ("Prepare", "Normalise audio or brief data and load only approved context."),
        ("Generate", "Transcribe, reason, synthesise speech or render video."),
        ("Observe", "Read real provider state, errors, timestamps and outputs."),
        ("Verify", "Apply safety, factual, media and release checks."),
        ("Deliver", "Return or publish through one authorised channel adapter."),
    ],
    statement=dict(
        headline="Generation is a stage. The workflow owns the outcome.",
        body="A reliable media agent proves what it received, what it generated, what it checked and where it delivered the result.",
        kicker="KEY IDEA",
    ),
    pillars_title="What You Will Build",
    pillars=[
        ("Voice Core", ["Browser audio -> Whisper", "AI Agent -> ElevenLabs", "Binary audio response"]),
        ("Voice Channel", ["Telegram voice-note adapter", "Session and fallback handling", "Phone-channel mapping"]),
        ("Video Pipeline", ["Governed script and profile", "Create and poll HeyGen job", "Approval and distribution"]),
    ],
    arc_title="How Every Lab Progresses",
    arc=[
        "Start from the same synthetic HarbourStay guest-experience scenario.",
        "Import a credential-free workflow template and reconnect only your own authorised credentials.",
        "Inspect the media and data contract before calling a provider.",
        "Run a positive path and one bounded failure path.",
        "Save a named evidence record so the next lab can reuse the verified checkpoint.",
    ],
)

LAB_SHOTS = {}

LG_INTRO = (
    "This guide teaches the architecture and operating decisions behind voice and video agents before walking through the n8n builds. "
    "The connected HarbourStay scenario begins with a browser voice concierge, reuses the same conversation core through a Telegram voice-note adapter, then turns approved service facts into an avatar welcome video and a governed distribution pipeline."
)
LG_INTRO2 = (
    "Every external service is called with a learner-owned account and placeholder credentials. Provider interfaces and pricing can change, so confirm the current official documentation linked in the references, keep clips short during practice and retain the request, status and output evidence described in each lab."
)
LG_SETUP = dict(
    needs=[
        "A laptop with a current Chromium-based browser and permission to use the microphone.",
        "An n8n Cloud workspace or a recent self-hosted n8n instance reachable from the browser and Telegram.",
        "An OpenAI API project with enough credit for short Whisper transcription and chat-model practice.",
        "An ElevenLabs account with an authorised voice and enough quota for short text-to-speech clips.",
        "A HeyGen account with API access, an authorised stock or custom avatar and voice, and quota for short test renders.",
        "A Telegram bot created through BotFather and, for Lab 4 distribution, a private test channel where the bot is an administrator.",
        "Python 3 is available to serve the browser lab apps; on Windows, the py launcher may be used when python is not on PATH.",
        "The C500 repository cloned locally; do not commit provider keys, tokens, generated customer data or private media.",
    ],
    verify_text="Open n8n, create a blank workflow and confirm that Webhook, HTTP Request, AI Agent, OpenAI Chat Model, Crypto, Data Table, Telegram, Wait and IF nodes are available. Import each starter JSON before editing it.",
    verify_code="python --version\n# Windows fallback: py --version\ngit clone https://github.com/tertiarycourses/C500-Voice-and-Video-Agents-with-n8n.git\ncd C500-Voice-and-Video-Agents-with-n8n\ngit status --short",
    conventions=[
        "Replace placeholders such as <OPENAI_HEADER_AUTH>, <ELEVENLABS_HEADER_AUTH>, <HEYGEN_HEADER_AUTH>, <TELEGRAM_CREDENTIAL> and <CHANNEL_ID> inside n8n with your own credential selections or test values.",
        "Use n8n credential storage for secrets. Do not paste API keys into prompts, workflow names, Sticky Notes, lab evidence or Git-tracked files.",
        "Use the Webhook Test URL while the workflow is listening in the editor; activate the workflow before changing an app to its Production URL.",
        "Keep every practice recording and video synthetic, short and free of real guest, employee or account information.",
        "A successful HTTP status is intermediate evidence; complete the lab only after the stated media output and failure-path check both succeed.",
    ],
)

LAB_NOTE = (
    "Use only synthetic HarbourStay data, voices, avatars, bots and channels that you are authorised to use. "
    "Keep secrets in n8n credentials, disclose synthetic media, and do not publish a generated asset outside the private training channel."
)

LG_WRAPUP = dict(
    title="Wrap-Up and Authoritative References",
    intro="You now have one reusable conversation core, two channel patterns and one governed asynchronous video pipeline. Recheck the official documentation before a production deployment because node and provider interfaces evolve.",
    sections=[
        dict(title="Official n8n references", bullets=[
            "Webhook node: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/",
            "AI Agent node: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/",
            "HTTP Request node: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/",
            "Telegram node: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.telegram/",
        ]),
        dict(title="Official provider references", bullets=[
            "OpenAI speech to text: https://platform.openai.com/docs/guides/speech-to-text",
            "ElevenLabs text to speech: https://elevenlabs.io/docs/api-reference/text-to-speech/convert",
            "HeyGen create avatar video: https://docs.heygen.com/reference/create-an-avatar-video-v2",
            "HeyGen video status: https://docs.heygen.com/reference/video-status",
            "Telegram Bot API: https://core.telegram.org/bots/api",
        ]),
        dict(title="Production readiness questions", bullets=[
            "Who owns each agent outcome, provider account, approved identity, destination and incident response?",
            "Which inputs, actions and channels are explicitly forbidden, and how is human handoff verified?",
            "What evidence proves factual accuracy, accessibility, consent, latency, cost and delivery?",
            "How are credentials rotated, media retained, duplicates prevented and published content corrected or removed?",
        ]),
    ],
)

LG_NEXT_STEPS = [
    "Replace the synthetic service facts with one approved, versioned knowledge source and retain its provenance.",
    "Extract the conversation core and video-render loop into reusable n8n sub-workflows with compact input/output contracts.",
    "Add dashboards for stage latency, failure classes, human handoffs, duplicate prevention and cost per accepted media asset.",
    "Pilot with internal users and private channels before enabling telephone numbers or public distribution.",
]

LG_GLOSSARY = [
    ("AI Agent", "A component that interprets an objective and chooses permitted actions within a defined role and workflow boundary."),
    ("Avatar", "The authorised visual identity rendered as the presenter in a synthetic video."),
    ("Binary data", "Non-text payload such as audio or video carried in a named n8n binary property."),
    ("Channel adapter", "Workflow logic that maps a browser, chat or phone event to and from the shared conversation contract."),
    ("Idempotency key", "A stable identifier used to prevent the same event from creating the same side effect more than once."),
    ("Speech to text", "Transcribing an audio signal into written words; in this course the provider pattern uses Whisper."),
    ("Synthetic media", "Audio or video generated or materially altered by an AI system."),
    ("Text to speech", "Synthesising spoken audio from approved response text; in this course the provider pattern uses ElevenLabs."),
    ("Webhook", "An HTTP endpoint that starts or continues a workflow when another system sends an event."),
]

NEXT_STEPS = dict(
    title="Implementation Roadmap",
    items=[
        "Pilot one informational use case with synthetic or approved low-risk data.",
        "Separate the conversation or render core from channel-specific adapters.",
        "Add consent, approval, retention, cost and human-handoff controls before broad access.",
        "Measure stage latency, errors, accepted outputs and cost before scaling volume.",
        "Revalidate provider contracts and permissions whenever a node, model, avatar or destination changes.",
    ],
)

THANK_YOU = dict(
    body="You can now design, build and verify connected voice and video agent workflows with n8n.",
    kicker="C500 | KEEP BUILDING RESPONSIBLY",
)

ICE_BREAKER = [
    "Your role and one communication process you would like to improve.",
    "Your current experience with n8n, voice interfaces or video creation.",
    "Which matters most for your use case: response speed, consistency, scale or accessibility?",
]

VERSION_HISTORY = [
    ("1.0", VERSION_DATE, "Initial aligned release: concept-first PPT, Learner Guide, Lesson Plan and four connected labs.", TRAINER),
]

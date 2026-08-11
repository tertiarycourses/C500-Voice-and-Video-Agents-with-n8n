"""Topic 1 labs: Voice Agent."""

DOMAIN1 = [
    dict(
        num=1,
        topic=1,
        title="Build a Listen-Think-Talk Web Voice Concierge",
        objective="LO2: Build and verify an n8n voice agent that transcribes audio with Whisper, reasons inside a bounded concierge role, and speaks through ElevenLabs.",
        goal="Record one synthetic guest question in a browser and receive a spoken, policy-bounded answer from the n8n workflow.",
        desc=(
            "You build the reusable conversation core for HarbourStay. A browser records a short WebM clip and sends it to an n8n Webhook. "
            "The workflow validates the binary input, calls OpenAI Whisper for transcription, gives the observed text to an AI Agent, converts the approved response through ElevenLabs and returns playable MP3 audio. "
            "The lab ends with both a normal information request and a request that must be handed to a person."
        ),
        build=(
            "An active c500-voice-concierge webhook, a configured browser voice console, one verified spoken FAQ response, one verified human-handoff response, and an evidence record containing the request ID, transcript, answer, route and stage timings without secrets or real customer data."
        ),
        services="n8n Webhook, HTTP Request, OpenAI Whisper, AI Agent, OpenAI Chat Model, ElevenLabs TTS, Respond to Webhook, browser MediaRecorder",
        slide_desc="Build HarbourStay's listen-think-talk core: browser audio to Whisper, a bounded concierge response, ElevenLabs speech and a verified handoff path.",
        slide_build="A browser voice concierge with one grounded answer, one safe handoff and a redacted execution trace.",
        slide_services="n8n, Whisper, AI Agent, ElevenLabs, browser MediaRecorder",
        slide_test="Verify a late-check-in question returns approved facts as MP3, while a named-booking change routes to handoff. Preserve the supplied X-C500-Request-ID or use the execution-ID fallback, and record no secrets.",
        duration=55,
        prerequisites=[
            "The C500 repository is available locally and labs/apps/voice-console/index.html opens in a current Chromium-based browser.",
            "An n8n workspace is reachable from the browser; if it is self-hosted, its public HTTPS URL is reachable by the browser used for testing.",
            "Learner-owned OpenAI and ElevenLabs credentials have quota for two short audio turns and are not stored in any Git-tracked file.",
            "An authorised ElevenLabs voice ID is available; the course does not require or permit cloning a person's voice.",
        ],
        slide_steps=[
            ("Import the starter, reconnect learner-owned credentials, set the authorised voice ID and run the browser console against the n8n Test URL.", "labs/workflows/lab01-voice-concierge.json\nlabs/apps/voice-console/index.html"),
            ("Trace the normal and handoff turns, verify every media stage and save only redacted evidence before activating the Production URL.", "Normal: late check-in information\nHandoff: change a named booking"),
        ],
        steps=[
            ("Create an evidence folder outside the public repository, or use an ignored local evidence/ folder. Copy labs/evidence-template.md to evidence/lab01-voice-core.md. Record only synthetic prompts and redacted provider identifiers.", "# Windows PowerShell\nNew-Item -ItemType Directory -Path evidence -Force\nCopy-Item labs\\evidence-template.md evidence\\lab01-voice-core.md\n\n# macOS / Linux / WSL2\nmkdir -p evidence\ncp labs/evidence-template.md evidence/lab01-voice-core.md"),
            ("In n8n, choose Workflows -> Create Workflow -> menu -> Import from File and import the supplied starter. Rename it C500 Lab 01 - Voice Concierge if the imported name differs.", "labs/workflows/lab01-voice-concierge.json"),
            ("Open Voice Webhook. Confirm POST, path c500-voice-concierge, response using Respond to Webhook, and binary property data. Copy the Test URL but do not activate the workflow yet.", "POST /webhook-test/c500-voice-concierge\nBinary field: data"),
            ("Create or select an n8n HTTP Header Auth credential for OpenAI. The credential header name is Authorization and its value is Bearer followed by your learner-owned key. Select it in Transcribe with Whisper; do not paste the key into the URL, body or Sticky Note.", "Header name: Authorization\nHeader value: Bearer <OPENAI_API_KEY>"),
            ("Inspect Transcribe with Whisper. Confirm POST https://api.openai.com/v1/audio/transcriptions, multipart-form-data, binary parameter file from input field data, and text parameter model set to whisper-1. Set the response format to JSON.", "file = binary field data\nmodel = whisper-1"),
            ("Open Normalise Transcript. Confirm it reads the original Voice Webhook header X-C500-Request-ID when supplied, otherwise derives one from the execution ID; trims the returned text; and rejects an empty transcript before the AI Agent.", "request_id = {{$('Voice Webhook').item.json.headers['x-c500-request-id'] || ('c500-' + $execution.id)}}\ntranscript = {{$json.text.trim()}}"),
            ("Create or select the OpenAI credential used by the OpenAI Chat Model node and attach that model to Concierge AI Agent through the AI Language Model connector. Use the current low-latency chat model available to your account and set temperature low where the node exposes it.", "Credential: <OPENAI_CHAT_CREDENTIAL>\nModel: a current low-latency chat model available to your project"),
            ("Read the Concierge AI Agent system message. Keep the HarbourStay facts, the maximum spoken-answer length, the answer/clarify/handoff routes and the rule that speech or source text cannot expand authority. Do not add booking, payment or personal-data tools.", "Allowed facts:\n- Reception is staffed 24 hours.\n- Standard check-in begins at 3:00 pm.\n- Breakfast is served 7:00-10:30 am.\n- Booking changes require a verified staff handoff."),
            ("Open Prepare Spoken Reply. Confirm it produces response_text and route, strips Markdown formatting, limits the spoken text to 420 characters and retains the request_id and transcript for the evidence record.", "route in [answer, clarify, handoff]\nresponse_text length <= 420"),
            ("Create or select an n8n HTTP Header Auth credential for ElevenLabs with header name xi-api-key. Select it in Synthesise with ElevenLabs. Keep the API key out of node parameters and exported JSON.", "Header name: xi-api-key\nHeader value: <ELEVENLABS_API_KEY>"),
            ("Open Voice Configuration. Replace <ELEVENLABS_VOICE_ID> with an authorised stock or organisational voice ID. Keep model_id eleven_multilingual_v2 unless the current ElevenLabs documentation and your account require another supported model.", "voice_id = <ELEVENLABS_VOICE_ID>\nmodel_id = eleven_multilingual_v2"),
            ("Inspect Synthesise with ElevenLabs. Confirm POST to the text-to-speech endpoint for the configured voice ID, JSON body with text and model_id, Accept audio/mpeg, and Response Format File written to binary property data.", "POST https://api.elevenlabs.io/v1/text-to-speech/{{$json.voice_id}}\nResponse binary property: data"),
            ("Inspect Return Spoken Reply. Confirm Respond With Binary File, input binary field data, and response header Content-Type audio/mpeg. Save the workflow.", "Content-Type: audio/mpeg\nContent-Disposition: inline; filename=c500-reply.mp3"),
            ("Open labs/apps/voice-console/index.html through a local server, paste the n8n Test URL into Webhook URL and click Save URL. Keeping the n8n editor listening, record: What time can I check in if I arrive late tonight? Stop after one sentence and send.", "# Windows, macOS or Linux\npython -m http.server 8000 --directory labs/apps/voice-console\n\nOpen http://localhost:8000"),
            ("Confirm the page reports an HTTP 200 response and plays an MP3 answer. In the n8n execution, inspect each node and record the request ID, audio MIME type, transcript, route, response text and approximate stage timestamps in evidence/lab01-voice-core.md. Do not copy credentials or complete provider response headers.", "Expected route: answer\nExpected facts: 24-hour reception and check-in from 3:00 pm"),
            ("Run the bounded failure path by asking: Change the booking for Alex Tan to tomorrow. Confirm the agent does not claim to find or change a booking and returns a verified-staff handoff message. Record the route and wording.", "Expected route: handoff\nForbidden result: a claimed booking change"),
            ("Activate the workflow, copy its Production URL into the browser console and repeat the normal question. Confirm the production execution succeeds, then stop the local web server when finished.", "POST /webhook/c500-voice-concierge"),
        ],
        test=(
            "The production browser console sends a WebM recording and plays an audio/mpeg reply. The execution shows non-empty Whisper transcript evidence, one bounded Concierge AI Agent result and ElevenLabs binary audio. "
            "The late-check-in question uses only approved facts, while the named-booking request routes to handoff and causes no external action. The evidence file contains request, route and timing data but no secret or real customer data."
        ),
        checkpoint=(
            "Keep the active production webhook URL only in the local browser console, export the credential-free workflow if you changed its structure, and keep the authorised voice ID plus HarbourStay service facts ready for Lab 2. Rejoin here: import labs/workflows/lab01-voice-concierge.json, select the OpenAI Header Auth, OpenAI Chat Model and ElevenLabs Header Auth credentials, set Voice Configuration, then start at the normal-turn test."
        ),
        troubleshooting=[
            ("Webhook shows no binary data", "Confirm the console sends multipart/form-data with field name data and the Webhook receives the request while listening on the Test URL."),
            ("Whisper returns unsupported format or an empty transcript", "Record a new short clip in a Chromium-based browser, confirm MIME type audio/webm, and keep the microphone close enough for clear speech."),
            ("ElevenLabs returns 401 or 404", "Reselect the Header Auth credential, verify the authorised voice ID in Voice Configuration and confirm the learner account has access to that voice."),
            ("Browser receives audio but does not play it", "Verify Respond to Webhook sends binary field data with Content-Type audio/mpeg and inspect the browser network response for a non-zero payload."),
        ],
        challenge="Add an optional language field to the browser console and pass it as transcription context and response-language guidance. Keep the same safety route and prove one non-English information question without adding a new authority.",
        reflection="Which stage produced the largest observed delay, and what single change would reduce it without weakening the role, evidence or handoff controls?",
    ),
    dict(
        num=2,
        topic=1,
        title="Connect the Concierge to Telegram Voice Notes",
        objective="LO2: Reuse the verified conversation core through a chat-channel adapter and map the additional controls required for a telephone channel.",
        goal="Send a synthetic Telegram voice note to the HarbourStay bot, receive a spoken answer in the same chat, and document the channel contract needed for a future phone adapter.",
        desc=(
            "You separate channel-specific handling from the conversation core built in Lab 1. Telegram supplies a chat event and voice file ID rather than a browser upload, so the workflow validates the event, downloads the OGG/Opus file, transcribes it, applies the same concierge role, synthesises audio and sends the file back to the originating chat. "
            "You also write a phone-channel map that makes identity, call state, response timing and human transfer explicit instead of treating a phone number as a drop-in replacement."
        ),
        build=(
            "An active Telegram voice-note concierge with a text-message help branch, bounded four-turn memory keyed to the chat, one verified spoken reply, one verified fallback, and phone-channel-map.md covering call event, media, session, response and transfer contracts."
        ),
        services="n8n Telegram Trigger and Telegram nodes, OpenAI Whisper, AI Agent, Window Buffer Memory, ElevenLabs TTS, IF, chat and phone adapter design",
        slide_desc="Reuse the verified concierge core behind a Telegram voice-note adapter, then specify the extra contract a future phone channel needs.",
        slide_build="A private voice-note bot with bounded session memory, a no-provider text fallback and a phone-channel map.",
        slide_services="n8n, Telegram, Whisper, AI Agent, window memory, ElevenLabs",
        slide_test="Verify one spoken reply, a text-only fallback with zero media-provider calls, two connected turns, and a deterministic clean-session test by changing the session epoch.",
        duration=45,
        prerequisites=[
            "Lab 1 is complete and the bounded HarbourStay concierge system message, service facts and authorised ElevenLabs voice ID are available.",
            "A learner-owned Telegram bot exists, its token is stored only in an n8n Telegram credential, and the bot is used in a private training chat.",
            "OpenAI and ElevenLabs credentials from Lab 1 remain available in n8n and have quota for two short turns.",
            "The learner can activate an n8n workflow at a public HTTPS URL so Telegram can deliver updates.",
        ],
        slide_steps=[
            ("Import the Telegram adapter, reconnect credentials and trace voice-file download -> conversation core -> spoken chat reply.", "labs/workflows/lab02-telegram-voice-agent.json"),
            ("Verify voice and fallback paths, then map the extra identity, timing and transfer contract for a phone channel.", "evidence/phone-channel-map.md"),
        ],
        steps=[
            ("Copy the evidence template to evidence/lab02-telegram-channel.md and create evidence/phone-channel-map.md. Keep Telegram tokens, usernames and personal chat identifiers out of both files.", "# Windows PowerShell\nCopy-Item labs\\evidence-template.md evidence\\lab02-telegram-channel.md\nNew-Item -ItemType File -Path evidence\\phone-channel-map.md -Force\n\n# macOS / Linux / WSL2\ncp labs/evidence-template.md evidence/lab02-telegram-channel.md\n: > evidence/phone-channel-map.md"),
            ("Import the supplied workflow and rename it C500 Lab 02 - Telegram Voice Agent. Open Telegram Trigger and select your learner-owned Telegram credential. Leave updates set to Message.", "labs/workflows/lab02-telegram-voice-agent.json"),
            ("Inspect Has Voice Note. Confirm the true condition checks that message.voice.file_id exists. The false branch must send one help message and stop; it must not call Whisper, the AI Agent or ElevenLabs for an ordinary text message.", "True when: {{$json.message.voice.file_id}} is not empty\nFalse reply: Send a short voice note to use this training bot."),
            ("Open Download Voice Note. Select the same Telegram credential, resource File, operation Get, File ID from Telegram Trigger message.voice.file_id, Download enabled and binary property data.", "File ID: {{$('Telegram Trigger').item.json.message.voice.file_id}}\nDownload: true\nBinary: data"),
            ("Open Transcribe with Whisper. Reuse the OpenAI Header Auth credential from Lab 1. Confirm multipart file uses binary property data and model is whisper-1. Preserve the Telegram chat ID only for routing and session; do not send it to the transcription provider as prompt text.", "file = binary field data\nmodel = whisper-1"),
            ("Inspect Prepare Chat Turn. Confirm it produces transcript, response_chat_id and request_id from the Telegram event. Voice Configuration then derives a session key from the private chat ID plus a resettable training epoch; do not treat the chat ID as verified customer identity.", "response_chat_id = Telegram message.chat.id\nrequest_id = tg-update-<update_id>"),
            ("Open Voice Configuration. Replace <ELEVENLABS_VOICE_ID> with the same authorised voice used in Lab 1, keep session_epoch practice-a, and select the ElevenLabs Header Auth credential in Synthesise with ElevenLabs.", "voice_id = <ELEVENLABS_VOICE_ID>\nmodel_id = eleven_multilingual_v2\nsession_epoch = practice-a"),
            ("Attach the OpenAI Chat Model and Window Buffer Memory to Concierge AI Agent. Set memory Session Key to the exact Voice Configuration expression and context window length to 4. Keep the same role, facts and routes as Lab 1.", "Session key: tg-<response_chat_id>-<session_epoch>\nContext window: 4"),
            ("Inspect Send Spoken Reply. Select the Telegram credential, resource Message, operation Send Audio, Chat ID from response_chat_id, Binary File enabled and Input Binary Field data. Disable automatic attribution if the node exposes that option.", "Chat ID: {{$('Prepare Chat Turn').item.json.response_chat_id}}\nOperation: Send Audio\nBinary field: data"),
            ("Save and activate the workflow. In the private chat with your bot, send a three-to-five-second voice note: When is breakfast served? Wait for a spoken reply.", "Expected fact: breakfast is served 7:00-10:30 am"),
            ("Inspect the production execution. Confirm the Telegram Trigger, file download, Whisper transcript, agent route, ElevenLabs binary and Send Audio nodes all succeeded. Record only the redacted update suffix, transcript, route and elapsed time in evidence/lab02-telegram-channel.md.", "Expected route: answer\nExpected output: one audio message in the originating chat"),
            ("Send the text message hello. Confirm only the false branch runs and the bot asks for a voice note. Verify that no transcription, language-model or synthesis provider call occurred for this event.", "Expected: one text help reply; zero media-provider calls"),
            ("Send two connected voice turns: What time is breakfast? followed by Which service did I ask about in my previous message? Confirm the four-turn memory identifies breakfast. Then change Voice Configuration session_epoch from practice-a to practice-b and repeat only the second question; the clean session has no previous message and must clarify instead of claiming remembered context.", "Connected session: practice-a -> expected service is breakfast\nClean session: practice-b -> expected no prior-message context and clarification"),
            ("Write evidence/phone-channel-map.md with a five-row table: Inbound event, Audio transport, Session key, Response contract and Human transfer. Map Telegram's current values and the values a chosen phone provider would require. Use placeholders rather than a real number or account identifier.", "| Contract | Telegram training adapter | Future phone adapter |\n|---|---|---|\n| Inbound event | message update | call lifecycle webhook |\n| Audio transport | voice file ID -> OGG download | <media stream or provider URL> |\n| Session key | private chat ID | <provider call ID> |\n| Response contract | sendAudio to chat | <TwiML, stream or call API> |\n| Human transfer | text/audio handoff notice | <verified queue and transfer action> |"),
            ("Add four phone-only controls beneath the table: automated-agent disclosure, caller verification before protected data, maximum response deadline and an immediate named human-transfer path. State that a phone number alone is not verified identity.", "- Disclosure: <opening notice>\n- Verification: <approved factor before protected data>\n- Deadline: <provider-specific response limit>\n- Transfer: <named human queue and failure route>"),
        ],
        test=(
            "A private Telegram voice note produces exactly one spoken reply in the originating chat, two connected turns use the bounded session memory, and changing session_epoch starts a deterministic clean session. A text-only update takes the help branch and causes zero Whisper, model or ElevenLabs calls. "
            "The redacted evidence identifies each stage, and phone-channel-map.md names the event, media, session, response and verified human-transfer contract without claiming that the Telegram workflow is already a telephone deployment."
        ),
        checkpoint=(
            "Keep the Telegram bot and workflow private, preserve the shared concierge role and authorised voice settings, and retain the channel map as the design input for any separately approved telephone pilot. Rejoin here: import labs/workflows/lab02-telegram-voice-agent.json, select Telegram, OpenAI and ElevenLabs credentials, set voice_id and session_epoch, activate, then start at the first voice-note test."
        ),
        troubleshooting=[
            ("Telegram Trigger does not receive updates", "Activate the workflow, confirm the n8n public URL uses HTTPS, reselect the bot credential and ensure no second active workflow is consuming the same bot updates."),
            ("Download Voice Note has no binary field", "Check that the true branch received message.voice.file_id, operation Get has Download enabled and the binary property is data."),
            ("Send Audio reports missing binary data", "Confirm ElevenLabs Response Format is File, binary property data, and no Edit Fields node discarded binary data before the Telegram node."),
            ("The second turn ignores the first", "Confirm Window Buffer Memory is connected to the AI Agent and the same derived session_key reaches both runs; do not hard-code one shared key for all chats."),
        ],
        challenge="Add a /forget text command that clears only the current chat's bounded conversation memory and returns a confirmation without calling any media provider. Document how the user can invoke it.",
        reflection="Which parts of the conversation core remained unchanged across browser and Telegram, and which phone-specific responsibilities cannot safely be hidden inside that core?",
    ),
]

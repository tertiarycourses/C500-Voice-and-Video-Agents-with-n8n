# Lab 2 — Connect the Concierge to Telegram Voice Notes

**Course:** Voice and Video Agents with n8n (C500)  
**Version:** v1.0  
**Release date:** 11 August 2026  
**Topic 1:** Voice Agent  
**Maps to:** LO2: Reuse the verified conversation core through a chat-channel adapter and map the additional controls required for a telephone channel.  
**Tools:** n8n Telegram Trigger and Telegram nodes, OpenAI Whisper, AI Agent, Window Buffer Memory, ElevenLabs TTS, IF, chat and phone adapter design

**Suggested duration:** 45 minutes  
**Prerequisites:**
- Lab 1 is complete and the bounded HarbourStay concierge system message, service facts and authorised ElevenLabs voice ID are available.
- A learner-owned Telegram bot exists, its token is stored only in an n8n Telegram credential, and the bot is used in a private training chat.
- OpenAI and ElevenLabs credentials from Lab 1 remain available in n8n and have quota for two short turns.
- The learner can activate an n8n workflow at a public HTTPS URL so Telegram can deliver updates.

---

## Goal

Send a synthetic Telegram voice note to the HarbourStay bot, receive a spoken answer in the same chat, and document the channel contract needed for a future phone adapter.

## What You Will Do

You separate channel-specific handling from the conversation core built in Lab 1. Telegram supplies a chat event and voice file ID rather than a browser upload, so the workflow validates the event, downloads the OGG/Opus file, transcribes it, applies the same concierge role, synthesises audio and sends the file back to the originating chat. You also write a phone-channel map that makes identity, call state, response timing and human transfer explicit instead of treating a phone number as a drop-in replacement.

## What You Will Build

An active Telegram voice-note concierge with a text-message help branch, bounded four-turn memory keyed to the chat, one verified spoken reply, one verified fallback, and phone-channel-map.md covering call event, media, session, response and transfer contracts.

> **Data note.** Use only synthetic HarbourStay data, voices, avatars, bots and channels that you are authorised to use. Keep secrets in n8n credentials, disclose synthetic media, and do not publish a generated asset outside the private training channel.

## Steps

**1. Copy the evidence template to evidence/lab02-telegram-channel.md and create evidence/phone-channel-map.md. Keep Telegram tokens, usernames and personal chat identifiers out of both files.**

```text
# Windows PowerShell
Copy-Item labs\evidence-template.md evidence\lab02-telegram-channel.md
New-Item -ItemType File -Path evidence\phone-channel-map.md -Force

# macOS / Linux / WSL2
cp labs/evidence-template.md evidence/lab02-telegram-channel.md
: > evidence/phone-channel-map.md
```

**2. Import the supplied workflow and rename it C500 Lab 02 - Telegram Voice Agent. Open Telegram Trigger and select your learner-owned Telegram credential. Leave updates set to Message.**

```text
labs/workflows/lab02-telegram-voice-agent.json
```

**3. Inspect Has Voice Note. Confirm the true condition checks that message.voice.file_id exists. The false branch must send one help message and stop; it must not call Whisper, the AI Agent or ElevenLabs for an ordinary text message.**

```text
True when: {{$json.message.voice.file_id}} is not empty
False reply: Send a short voice note to use this training bot.
```

**4. Open Download Voice Note. Select the same Telegram credential, resource File, operation Get, File ID from Telegram Trigger message.voice.file_id, Download enabled and binary property data.**

```text
File ID: {{$('Telegram Trigger').item.json.message.voice.file_id}}
Download: true
Binary: data
```

**5. Open Transcribe with Whisper. Reuse the OpenAI Header Auth credential from Lab 1. Confirm multipart file uses binary property data and model is whisper-1. Preserve the Telegram chat ID only for routing and session; do not send it to the transcription provider as prompt text.**

```text
file = binary field data
model = whisper-1
```

**6. Inspect Prepare Chat Turn. Confirm it produces transcript, response_chat_id and request_id from the Telegram event. Voice Configuration then derives a session key from the private chat ID plus a resettable training epoch; do not treat the chat ID as verified customer identity.**

```text
response_chat_id = Telegram message.chat.id
request_id = tg-update-<update_id>
```

**7. Open Voice Configuration. Replace <ELEVENLABS_VOICE_ID> with the same authorised voice used in Lab 1, keep session_epoch practice-a, and select the ElevenLabs Header Auth credential in Synthesise with ElevenLabs.**

```text
voice_id = <ELEVENLABS_VOICE_ID>
model_id = eleven_multilingual_v2
session_epoch = practice-a
```

**8. Attach the OpenAI Chat Model and Window Buffer Memory to Concierge AI Agent. Set memory Session Key to the exact Voice Configuration expression and context window length to 4. Keep the same role, facts and routes as Lab 1.**

```text
Session key: tg-<response_chat_id>-<session_epoch>
Context window: 4
```

**9. Inspect Send Spoken Reply. Select the Telegram credential, resource Message, operation Send Audio, Chat ID from response_chat_id, Binary File enabled and Input Binary Field data. Disable automatic attribution if the node exposes that option.**

```text
Chat ID: {{$('Prepare Chat Turn').item.json.response_chat_id}}
Operation: Send Audio
Binary field: data
```

**10. Save and activate the workflow. In the private chat with your bot, send a three-to-five-second voice note: When is breakfast served? Wait for a spoken reply.**

```text
Expected fact: breakfast is served 7:00-10:30 am
```

**11. Inspect the production execution. Confirm the Telegram Trigger, file download, Whisper transcript, agent route, ElevenLabs binary and Send Audio nodes all succeeded. Record only the redacted update suffix, transcript, route and elapsed time in evidence/lab02-telegram-channel.md.**

```text
Expected route: answer
Expected output: one audio message in the originating chat
```

**12. Send the text message hello. Confirm only the false branch runs and the bot asks for a voice note. Verify that no transcription, language-model or synthesis provider call occurred for this event.**

```text
Expected: one text help reply; zero media-provider calls
```

**13. Send two connected voice turns: What time is breakfast? followed by Which service did I ask about in my previous message? Confirm the four-turn memory identifies breakfast. Then change Voice Configuration session_epoch from practice-a to practice-b and repeat only the second question; the clean session has no previous message and must clarify instead of claiming remembered context.**

```text
Connected session: practice-a -> expected service is breakfast
Clean session: practice-b -> expected no prior-message context and clarification
```

**14. Write evidence/phone-channel-map.md with a five-row table: Inbound event, Audio transport, Session key, Response contract and Human transfer. Map Telegram's current values and the values a chosen phone provider would require. Use placeholders rather than a real number or account identifier.**

```text
| Contract | Telegram training adapter | Future phone adapter |
|---|---|---|
| Inbound event | message update | call lifecycle webhook |
| Audio transport | voice file ID -> OGG download | <media stream or provider URL> |
| Session key | private chat ID | <provider call ID> |
| Response contract | sendAudio to chat | <TwiML, stream or call API> |
| Human transfer | text/audio handoff notice | <verified queue and transfer action> |
```

**15. Add four phone-only controls beneath the table: automated-agent disclosure, caller verification before protected data, maximum response deadline and an immediate named human-transfer path. State that a phone number alone is not verified identity.**

```text
- Disclosure: <opening notice>
- Verification: <approved factor before protected data>
- Deadline: <provider-specific response limit>
- Transfer: <named human queue and failure route>
```

## Test It

A private Telegram voice note produces exactly one spoken reply in the originating chat, two connected turns use the bounded session memory, and changing session_epoch starts a deterministic clean session. A text-only update takes the help branch and causes zero Whisper, model or ElevenLabs calls. The redacted evidence identifies each stage, and phone-channel-map.md names the event, media, session, response and verified human-transfer contract without claiming that the Telegram workflow is already a telephone deployment.

## Checkpoint

Keep the Telegram bot and workflow private, preserve the shared concierge role and authorised voice settings, and retain the channel map as the design input for any separately approved telephone pilot. Rejoin here: import labs/workflows/lab02-telegram-voice-agent.json, select Telegram, OpenAI and ElevenLabs credentials, set voice_id and session_epoch, activate, then start at the first voice-note test.

## Troubleshooting

- **Telegram Trigger does not receive updates** — Activate the workflow, confirm the n8n public URL uses HTTPS, reselect the bot credential and ensure no second active workflow is consuming the same bot updates.
- **Download Voice Note has no binary field** — Check that the true branch received message.voice.file_id, operation Get has Download enabled and the binary property is data.
- **Send Audio reports missing binary data** — Confirm ElevenLabs Response Format is File, binary property data, and no Edit Fields node discarded binary data before the Telegram node.
- **The second turn ignores the first** — Confirm Window Buffer Memory is connected to the AI Agent and the same derived session_key reaches both runs; do not hard-code one shared key for all chats.

## Challenge

Add a /forget text command that clears only the current chat's bounded conversation memory and returns a confirmation without calling any media provider. Document how the user can invoke it.

## Reflection

Which parts of the conversation core remained unchanged across browser and Telegram, and which phone-specific responsibilities cannot safely be hidden inside that core?

---

[← Lab 1](lab-01-build-a-listen-think-talk-web-voice-concierge.md) · [Lab 3 →](lab-03-generate-a-talking-head-welcome-video.md)

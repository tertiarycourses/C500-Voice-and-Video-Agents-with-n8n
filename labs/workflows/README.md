# C500 n8n Workflow Starters

| Lab | Starter | Purpose |
|---|---|---|
| 1 | `lab01-voice-concierge.json` | Browser audio -> Whisper -> AI Agent -> ElevenLabs -> binary reply |
| 2 | `lab02-telegram-voice-agent.json` | Telegram voice note -> shared concierge core -> spoken chat reply |
| 3 | `lab03-avatar-video.json` | Draft + native-Crypto SHA-256 snapshot -> exact script/disclosure approval -> HeyGen create-once/status loop |
| 3 recovery | `lab03-status-resume.json` | Known HeyGen video ID -> bounded status checks only; no create call |
| 4 | `lab04-video-campaign-pipeline.json` | Persistent queue/run tables -> native-Crypto hash checks -> create once -> private Telegram distribution |

Import a starter through n8n's **Import from File** command. Every credential selection and account-specific asset ID is intentionally absent. Follow the matching `labs/lab-NN-*.md` file to configure and verify the workflow.

Provider and node interfaces evolve. Compare the starter with the current official documentation linked from `reference/research-sources.md`, especially before using a paid render or enabling a schedule.

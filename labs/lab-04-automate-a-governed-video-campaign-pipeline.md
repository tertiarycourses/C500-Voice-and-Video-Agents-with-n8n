# Lab 4 — Automate a Governed Video Campaign Pipeline

**Course:** Voice and Video Agents with n8n (C500)  
**Version:** v1.0  
**Release date:** 11 August 2026  
**Topic 2:** Video Agent  
**Maps to:** LO4: Automate an approved script snapshot through persistent idempotency, avatar rendering, release checks and private-channel distribution with recoverable operating evidence.  
**Tools:** n8n Schedule Trigger, Manual Trigger, Data Table, Code, HeyGen API, Wait, IF, Telegram Send Video, persistent ledger, release runbook

**Suggested duration:** 50 minutes  
**Prerequisites:**
- Lab 3 is complete with an approved script snapshot, authorised profile and a verified create-once/status-only contract.
- A private Telegram training channel exists and the learner-owned bot is an administrator; its destination ID is reviewed but not committed to Git.
- The n8n workspace provides Data Tables and the HeyGen and Telegram credentials used in the prior labs.
- Quota is available for no more than one additional short render unless the trainer explicitly authorises more.

---

## Goal

Process one approved synthetic queue row, publish its completed video to a private Telegram test channel, and prove replay causes neither a duplicate render nor a duplicate post.

## What You Will Do

You operationalise the Lab 3 contract with two n8n Data Tables. The queue stores an exact approved script hash, campaign profile version and destination; the run ledger persists an idempotency key before any paid render. Provider errors, failed release checks and timeouts update the same ledger row to review_required with a known video ID when available. A replay stops at the persistent existence check.

## What You Will Build

A c500_campaign_queue approval table, c500_campaign_runs ledger, scheduled-but-disabled n8n pipeline, one privately distributed training video, a duplicate-skip trace, status-only recovery path and an operating runbook.

> **Data note.** Use only synthetic HarbourStay data, voices, avatars, bots and channels that you are authorised to use. Keep secrets in n8n credentials, disclose synthetic media, and do not publish a generated asset outside the private training channel.

## Steps

**1. Copy the evidence template to evidence/lab04-campaign-pipeline.md and create evidence/video-agent-runbook.md. Use synthetic identifiers and name a learner operator plus trainer release reviewer.**

```text
# Windows PowerShell
Copy-Item labs\evidence-template.md evidence\lab04-campaign-pipeline.md
New-Item -ItemType File -Path evidence\video-agent-runbook.md -Force

# macOS / Linux / WSL2
cp labs/evidence-template.md evidence/lab04-campaign-pipeline.md
: > evidence/video-agent-runbook.md
```

**2. Create Data Table c500_campaign_queue with the exact columns below. approved_script, approved_script_hash, approved_profile_version and approved_destination_id form the trusted release snapshot.**

```text
campaign_id:string
approved_script:string
approved_script_hash:string
approved_profile_version:string
approved_destination_id:string
approval_status:string
requested_by:string
```

**3. Create Data Table c500_campaign_runs with the exact persistent ledger columns. request_key is the replay guard; status and error_class preserve terminal or review state.**

```text
campaign_id:string
request_key:string
status:string
video_id:string
video_url:string
destination_id:string
message_id:string
attempts:number
script_hash:string
profile_version:string
started_at:dateTime
completed_at:dateTime
error_class:string
```

**4. Add one queue row from the exact approved Lab 3 snapshot. Set campaign_id c500-weekly-tip-001, copy the approved script and SHA-256 exactly, use profile version c500-demo-1, your private destination ID and approval_status pending.**

```text
campaign_id: c500-weekly-tip-001
approved_script: <exact Lab 3 script>
approved_script_hash: <exact SHA-256>
approved_profile_version: c500-demo-1
approved_destination_id: <private channel ID>
approval_status: pending
```

**5. Import C500 Lab 04 - Video Campaign Pipeline. Keep Schedule Trigger disabled and use Manual Trigger. Confirm Get Approved Campaign is an actual Data Table Row/Get operation filtered to campaign_id c500-weekly-tip-001.**

```text
labs/workflows/lab04-video-campaign-pipeline.json
Table: c500_campaign_queue
Operation: Row / Get
```

**6. Inspect Approval Gate. Only approval_status exactly approved reaches Pipeline Configuration and the persistent run query. Pending content routes to Record Unapproved Skip and stops before HeyGen or Telegram.**

```text
pending -> skipped_unapproved
approved -> validate snapshot -> query ledger
```

**7. Inspect Find Existing Run. It is a Data Table Row/Get operation on c500_campaign_runs filtered by request_key c500-video:<campaign_id>, limited to one row and configured to output an empty item when no row exists. Classify Existing Run routes an existing row to Record Duplicate Skip and a no-row result to Insert Run Ledger.**

```text
request_key = c500-video:<campaign_id>
existing row -> skipped_duplicate
no row -> Insert Run Ledger
```

**8. Run the pending row. Confirm Insert Run Ledger, Create Avatar Video and Publish Private Preview do not execute. Record skipped_unapproved and zero external calls.**

```text
Expected external provider calls: 0
Expected ledger inserts: 0
```

**9. Review the exact script, hash, profile version and private destination, then change only approval_status to approved. Open Pipeline Configuration and set authorised avatar_id, voice_id, profile_version c500-demo-1, poll_seconds 15 and maximum_poll_attempts 20.**

```text
approval_status: approved
profile_version: c500-demo-1
maximum_poll_attempts: 20
```

**10. Inspect Validate Approved Snapshot and Hash Queue Script. The Code node checks required snapshot fields and profile version; the native n8n Crypto node writes SHA-256 into script_hash. Approved Snapshot Valid requires exact equality with approved_script_hash and a non-empty approved_destination_id. A mismatch stops before ledger insert and provider calls.**

```text
Hash Queue Script: SHA256(approved_script) -> script_hash
script_hash = approved_script_hash
approved_profile_version = configured profile_version
```

**11. Select HeyGen credentials in Create Avatar Video and Check Video Status. Confirm Insert Run Ledger writes request_key and status rendering before Create, and Store Provider Video ID updates that same row immediately after a successful create response.**

```text
insert status: rendering
create calls: at most 1
update video_id: before Wait
```

**12. Inspect error wiring. Create and status HTTP error outputs, failed state, timeout and failed Release Checks all reach Mark Review Required, which updates the same request_key with status review_required, error_class and the known video_id when available.**

```text
error -> review_required
known video_id retained
never route error to Create
```

**13. Inspect Wait, Check Video Status and Route Status. Processing increments attempts and loops to Wait; completed goes to Release Checks; failed or attempt 20 goes to Mark Review Required. No loop returns to Create Avatar Video.**

```text
processing -> Wait
completed -> Release Checks
failed|timeout -> Mark Review Required
```

**14. Inspect Hash Release Script and Release Checks. The native Crypto node recomputes the script hash; Release Checks requires completed status, non-empty video_url, exact hash and profile matches, then passes through only the trusted approved_destination_id from the queue snapshot. No provider or publish response may replace that destination.**

```text
Required: completed + video_url + exact hash + exact profile
Publish destination source: approved queue snapshot only
```

**15. Open Publish Private Preview. Select the Telegram credential, Send Video by URL, Chat ID from approved_destination_id and a caption that includes synthetic-media disclosure. Its error output must also reach Mark Review Required.**

```text
Video: {{$json.video_url}}
Chat ID: {{$json.approved_destination_id}}
Caption suffix: Generated with an AI avatar - training preview.
```

**16. Inspect Mark Published. It updates the existing c500_campaign_runs row filtered by request_key with status published, video ID and URL, Telegram message ID, attempts, exact hash, profile version and completed_at.**

```text
Operation: Data Table Row / Update
Filter: request_key
status: published
```

**17. Run the approved row once. Observe one ledger insert, one create call, the known video ID through bounded polling, one private disclosed Telegram post and one published update.**

```text
Expected ledger rows for request_key: 1
Expected create calls: 1
Expected Telegram posts: 1
```

**18. Replay with Manual Trigger. Confirm Find Existing Run returns the persisted row and Record Duplicate Skip executes; Insert Run Ledger, HeyGen and Telegram must not execute. Save the execution trace.**

```text
Expected: skipped_duplicate
Additional create calls: 0
Additional Telegram posts: 0
```

**19. Complete the runbook with owners, source and snapshot rules, schedule, maximum one video per run, poll deadline, monthly usage limit, monitoring, status-only recovery, credential rotation, retention, private-to-public review and rollback. Leave Schedule Trigger disabled. Save a node-by-node diff checklist naming only credential selectors, authorised IDs and Data Table bindings changed from the starter.**

```text
Recovery: labs/workflows/lab03-status-resume.json
Timezone: Asia/Singapore
Example schedule: Monday 09:00
Final schedule state: disabled
Diff: tables + credentials + authorised IDs only
```

## Test It

Pending content causes zero ledger inserts and zero external calls. The exact approved snapshot inserts one persistent request key before one create call, stores the returned video ID, reaches published or review_required through bounded polling, and writes every error path to the ledger. A published run sends one disclosed private video, while replay resolves through the persistent existing-row query with zero additional render or Telegram calls. A known timed-out job can be checked through the status-only workflow without calling create.

## Checkpoint

Leave Schedule Trigger disabled and retain the synthetic queue row, persistent run-ledger row, private preview, duplicate-skip trace and runbook. Rejoin here: import labs/workflows/lab04-video-campaign-pipeline.json, bind both Data Tables and credentials, set Pipeline Configuration, confirm approval snapshot hash, then run Manual Trigger; for any retained video_id use labs/workflows/lab03-status-resume.json and never rerun Create.

## Troubleshooting

- **A pending row reaches HeyGen** — Stop the run and confirm Approval Gate is before Validate Approved Snapshot, both existence checks, ledger insert and every external provider node.
- **A replay creates another video** — Disable the workflow, confirm request_key is identical, bind both Data Table existence operations to c500_campaign_runs and restore the rowNotExists/rowExists branches before Create.
- **Ledger remains rendering after a provider error** — Connect the HTTP error output to Mark Review Required and update the same request_key with error_class plus any known video_id.
- **Telegram cannot send the video URL** — Keep the run ledger, mark review_required, verify bot access and approved_destination_id, then retry only the publish stage after human review; never create another video.

## Challenge

Add an approval-expiry timestamp to the trusted queue snapshot and prove an expired row fails before ledger insert, HeyGen or Telegram.

## Reflection

What production database constraint would make the persistent request_key guarantee atomic when two scheduler executions start at the same instant?

---

[← Lab 3](lab-03-generate-a-talking-head-welcome-video.md) · [Labs index →](README.md)

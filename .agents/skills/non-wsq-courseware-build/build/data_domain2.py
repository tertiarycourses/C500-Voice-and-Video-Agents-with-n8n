"""Topic 2 labs: Video Agent."""

DOMAIN2 = [
    dict(
        num=3,
        topic=2,
        title="Generate a Talking-Head Welcome Video",
        objective="LO3: Build and verify a two-phase n8n avatar-video workflow that binds human approval to an exact script hash before one asynchronous render.",
        goal="Generate a synthetic HarbourStay script draft, approve that exact hashed draft, and receive one completed talking-head video URL with a traceable provider job ID.",
        desc=(
            "You build a two-phase avatar-video workflow. A draft request turns approved facts into structured copy and returns the script plus its SHA-256 hash without calling HeyGen. "
            "A separate render request supplies the exact approved script and hash; n8n recomputes the hash, binds it to an authorised campaign profile, creates one video job and polls only that known job. A status-only starter lets an operator resume after the polling deadline without creating again."
        ),
        build=(
            "A draft-and-render n8n webhook, a browser Video Studio that preserves the reviewed script snapshot, one authorised 16:9 captioned avatar video, a status-only resume workflow, and redacted evidence linking brief, script hash, profile version, video ID, attempts and terminal state."
        ),
        services="n8n Webhook, AI Agent, OpenAI Chat Model, Code, HTTP Request, HeyGen API, Wait, IF, Respond to Webhook, browser Video Studio",
        slide_desc="Build a two-phase video agent: generate a hashed draft, approve that exact snapshot, create one HeyGen job and poll only its stored video ID.",
        slide_build="A draft/render webhook, approval-bound browser studio, one captioned video and a status-only resume path.",
        slide_services="n8n, OpenAI Chat Model, HeyGen API, browser Video Studio",
        slide_test="Prove draft mode makes zero HeyGen calls, render mode rejects a changed script or hash, and one approved snapshot creates one stored video ID that reaches a bounded terminal state.",
        duration=55,
        prerequisites=[
            "Labs 1 and 2 are complete and the approved HarbourStay service facts are available as synthetic source material.",
            "A learner-owned OpenAI model credential and HeyGen API credential are stored in n8n; no secret appears in exported JSON.",
            "An authorised HeyGen avatar ID and voice ID are available, with quota for one short 1280x720 training render.",
            "Python 3 is available to serve labs/apps/video-studio; on Windows, py -m http.server is an equivalent fallback.",
        ],
        slide_steps=[
            ("Import the two-phase workflow, reconnect credentials and generate one structured draft with an exact SHA-256 approval hash.", "labs/workflows/lab03-avatar-video.json"),
            ("Approve the unchanged snapshot, create one video ID, poll it to a terminal state and use the status-only resume path if the deadline expires.", "labs/workflows/lab03-status-resume.json"),
        ],
        steps=[
            ("Copy the evidence template to evidence/lab03-avatar-video.md. Record only synthetic content, hash and provider-ID suffixes; never paste complete credentials or private provider responses.", "# Windows PowerShell\nCopy-Item labs\\evidence-template.md evidence\\lab03-avatar-video.md\n\n# macOS / Linux / WSL2\ncp labs/evidence-template.md evidence/lab03-avatar-video.md"),
            ("Import the supplied workflow and rename it C500 Lab 03 - Avatar Video. Confirm Avatar Video Webhook uses POST path c500-avatar-video and Respond to Webhook. Copy its Test URL.", "labs/workflows/lab03-avatar-video.json\nPOST /webhook-test/c500-avatar-video"),
            ("Open Validate Request. Confirm action must be draft or render. Draft requires brief_id, audience, objective, approved_facts, call_to_action and max_words 30-90. Render requires brief_id, approved_script, approved_script_hash, approved_disclosure and approved_for_render true.", "action: draft | render\ndraft max_words: 30..90\nrender approved_for_render: true"),
            ("Inspect Is Draft Request. Its true path alone reaches Script Agent; its false path goes directly to Validate Approved Draft. There must be no path from a render request back through the model.", "draft -> Script Agent\nrender -> Validate Approved Draft\nrender -> Script Agent: forbidden"),
            ("Attach a learner-owned OpenAI Chat Model to Script Agent. Keep its contract: use only approved_facts and return title, spoken_script, caption, claim_list and disclosure; do not invent prices, availability, testimonials or guarantees.", "Output: title, spoken_script, caption, claim_list, disclosure"),
            ("Inspect Build Draft Snapshot and Hash Draft Script. Confirm the Code node extracts JSON even when the model wraps it in backtick or tilde fences, checks word count and claim subset, and requires disclosure. The native n8n Crypto node then writes a SHA-256 script_hash over the exact spoken_script without Code-node module imports.", "script_contract_ok = true\nHash Draft Script: SHA256(exact spoken_script) -> script_hash"),
            ("Open Return Draft. Confirm it returns status draft_ready, brief_id, exact spoken_script, script_hash, caption, disclosure, claim_list and profile_id. It must not run Campaign Profile or Create Avatar Video.", "Expected draft status: draft_ready\nExpected HeyGen create calls: 0"),
            ("Open Video Studio through a local server, paste the Test URL and click Generate Draft. If python is unavailable on Windows, use the py fallback. Keep the n8n workflow listening.", "python -m http.server 8001 --directory labs/apps/video-studio\n# Windows fallback\npy -m http.server 8001 --directory labs/apps/video-studio\n\nOpen http://localhost:8001"),
            ("Review the displayed script, disclosure and hash. Use only the Approve Exact Draft & Render button; it must send the stored spoken_script, disclosure and script_hash without asking the model for another script.", "action = render\napproved_script = exact draft text\napproved_script_hash = displayed SHA-256\napproved_disclosure = exact draft disclosure\napproved_for_render = true"),
            ("Before a paid render, change one character in approved_script with browser developer tools or an API client while keeping the old hash. Confirm Hash Approved Script and Approval Snapshot Valid route to approval_mismatch and Create Avatar Video does not run.", "Expected: approval_mismatch\nExpected HeyGen create calls: 0"),
            ("Open Campaign Profile. Replace <HEYGEN_AVATAR_ID> and <HEYGEN_VOICE_ID> with authorised assets. Keep profile_version c500-demo-1, width 1280, height 720, captions true and destination private-preview.", "avatar_id = <HEYGEN_AVATAR_ID>\nvoice_id = <HEYGEN_VOICE_ID>\nprofile_version = c500-demo-1"),
            ("Select an n8n HTTP Header Auth credential for HeyGen with header X-Api-Key in Create Avatar Video and Check Video Status. Confirm Create uses the exact approved_script followed by the approved synthetic-media disclosure, authorised IDs, 1280x720 dimensions and captions.", "POST https://api.heygen.com/v2/video/generate\nHeader: X-Api-Key from n8n credential\nvoice.input_text = approved_script + approved_disclosure"),
            ("Inspect both HTTP nodes. Continue On Fail or the error output must route provider errors to Normalise Provider Error, which returns review_required with error_class and any known video_id rather than stopping before evidence is written.", "create/status error -> Normalise Provider Error -> Return Provider Error"),
            ("Click Approve Exact Draft & Render once. Confirm Store Job records brief_id, approved_script_hash, approved_disclosure, profile_version, returned video_id, poll_attempt 0 and created_at before Wait. Never retry Create Avatar Video.", "Expected create calls: 1\nRequired stored fields: video_id and approved_disclosure\npoll_attempt = 0"),
            ("Trace Wait for Render, Check Video Status and Route Status. Processing increments poll_attempt and returns to Wait; completed returns the URLs; failed and the 20-attempt deadline return review_required while preserving the known video_id.", "Wait: 15 seconds\nMaximum status attempts: 20\nprocessing -> Wait; never -> Create"),
            ("If the deadline is reached, import C500 Lab 03 - Status Resume, set Known Job.video_id to the retained value, select the HeyGen credential and run it. Confirm this workflow contains no create endpoint and performs status checks only.", "labs/workflows/lab03-status-resume.json\nGET /v1/video_status.get?video_id=<known video_id>\nCreate endpoint count: 0"),
            ("For a completed job, compare the rendered speech and captions with the exact approved_script; confirm authorised avatar, voice, 16:9 framing, disclosure and no unsupported claim. Record discrepancies as review_required.", "Release evidence: script hash, identity, voice, captions, framing, disclosure"),
            ("Activate the main workflow and replace the Video Studio URL with its Production URL. Save a final node-by-node diff checklist in evidence: imported node names, changed credential selectors, avatar ID, voice ID, webhook URL, and no other structural changes.", "POST /webhook/c500-avatar-video\nDiff: credentials + authorised IDs + URL only"),
        ],
        test=(
            "Draft mode returns a valid structured script and SHA-256 hash with zero HeyGen calls. A changed script with the old hash fails closed. The exact approved snapshot creates one job, stores its video_id before bounded status polling, and ends completed or review_required without duplicate creation. "
            "A timed-out job can resume through the status-only workflow, and completed evidence binds the exact script hash, profile version, video ID and final asset without exposing credentials."
        ),
        checkpoint=(
            "Keep the credential-free main and status-only workflows, authorised campaign profile, approved script snapshot and completed Lab 3 evidence. Rejoin here: import labs/workflows/lab03-avatar-video.json, select OpenAI and HeyGen credentials, set Campaign Profile, generate a fresh draft, approve that exact hash, then resume from Store Job using labs/workflows/lab03-status-resume.json only if a known video_id has timed out."
        ),
        troubleshooting=[
            ("The approved render produces a different script", "Stop: render requests must bypass Script Agent. Send the exact draft as approved_script and compare its recomputed SHA-256 with approved_script_hash before Campaign Profile."),
            ("Create Avatar Video returns an error", "Inspect Normalise Provider Error, compare the current official schema, confirm authorised IDs and preserve review_required evidence without retrying create."),
            ("Status remains processing beyond the lab", "Retain the original video_id and use lab03-status-resume.json; never submit the brief to the create endpoint again."),
            ("Video content differs from the snapshot", "Mark review_required, preserve both artefacts and create a separately approved new snapshot rather than editing evidence."),
        ],
        challenge="Add a second approved 1080x1920 campaign profile. Bind its version into the approval snapshot and prove an unknown profile or mismatched version fails before the create call.",
        reflection="Which exact values must be frozen at approval so a later render is demonstrably the media a reviewer authorised?",
    ),
    dict(
        num=4,
        topic=2,
        title="Automate a Governed Video Campaign Pipeline",
        objective="LO4: Automate an approved script snapshot through persistent idempotency, avatar rendering, release checks and private-channel distribution with recoverable operating evidence.",
        goal="Process one approved synthetic queue row, publish its completed video to a private Telegram test channel, and prove replay causes neither a duplicate render nor a duplicate post.",
        desc=(
            "You operationalise the Lab 3 contract with two n8n Data Tables. The queue stores an exact approved script hash, campaign profile version and destination; the run ledger persists an idempotency key before any paid render. "
            "Provider errors, failed release checks and timeouts update the same ledger row to review_required with a known video ID when available. A replay stops at the persistent existence check."
        ),
        build=(
            "A c500_campaign_queue approval table, c500_campaign_runs ledger, scheduled-but-disabled n8n pipeline, one privately distributed training video, a duplicate-skip trace, status-only recovery path and an operating runbook."
        ),
        services="n8n Schedule Trigger, Manual Trigger, Data Table, Code, HeyGen API, Wait, IF, Telegram Send Video, persistent ledger, release runbook",
        slide_desc="Operate one approved video snapshot through persistent queue and run tables, create-once rendering, exact release checks and private distribution.",
        slide_build="A disabled schedule, persistent idempotency ledger, one private release, duplicate-skip proof and recovery runbook.",
        slide_services="n8n Data Table, HeyGen API, Telegram, Wait, IF, Code",
        slide_test="Verify pending content makes zero external calls, one approved key produces one render and one private post, provider failures write review_required, and replay skips before create.",
        duration=50,
        prerequisites=[
            "Lab 3 is complete with an approved script snapshot, authorised profile and a verified create-once/status-only contract.",
            "A private Telegram training channel exists and the learner-owned bot is an administrator; its destination ID is reviewed but not committed to Git.",
            "The n8n workspace provides Data Tables and the HeyGen and Telegram credentials used in the prior labs.",
            "Quota is available for no more than one additional short render unless the trainer explicitly authorises more.",
        ],
        slide_steps=[
            ("Create the exact queue and ledger schemas, import the pipeline and verify approval plus a persistent existing-run query before any provider call.", "labs/workflows/lab04-video-campaign-pipeline.json"),
            ("Release once, prove the persisted request key blocks replay, and recover any known timed-out job through the status-only workflow.", "labs/workflows/lab03-status-resume.json"),
        ],
        steps=[
            ("Copy the evidence template to evidence/lab04-campaign-pipeline.md and create evidence/video-agent-runbook.md. Use synthetic identifiers and name a learner operator plus trainer release reviewer.", "# Windows PowerShell\nCopy-Item labs\\evidence-template.md evidence\\lab04-campaign-pipeline.md\nNew-Item -ItemType File -Path evidence\\video-agent-runbook.md -Force\n\n# macOS / Linux / WSL2\ncp labs/evidence-template.md evidence/lab04-campaign-pipeline.md\n: > evidence/video-agent-runbook.md"),
            ("Create Data Table c500_campaign_queue with the exact columns below. approved_script, approved_script_hash, approved_profile_version and approved_destination_id form the trusted release snapshot.", "campaign_id:string\napproved_script:string\napproved_script_hash:string\napproved_profile_version:string\napproved_destination_id:string\napproval_status:string\nrequested_by:string"),
            ("Create Data Table c500_campaign_runs with the exact persistent ledger columns. request_key is the replay guard; status and error_class preserve terminal or review state.", "campaign_id:string\nrequest_key:string\nstatus:string\nvideo_id:string\nvideo_url:string\ndestination_id:string\nmessage_id:string\nattempts:number\nscript_hash:string\nprofile_version:string\nstarted_at:dateTime\ncompleted_at:dateTime\nerror_class:string"),
            ("Add one queue row from the exact approved Lab 3 snapshot. Set campaign_id c500-weekly-tip-001, copy the approved script and SHA-256 exactly, use profile version c500-demo-1, your private destination ID and approval_status pending.", "campaign_id: c500-weekly-tip-001\napproved_script: <exact Lab 3 script>\napproved_script_hash: <exact SHA-256>\napproved_profile_version: c500-demo-1\napproved_destination_id: <private channel ID>\napproval_status: pending"),
            ("Import C500 Lab 04 - Video Campaign Pipeline. Keep Schedule Trigger disabled and use Manual Trigger. Confirm Get Approved Campaign is an actual Data Table Row/Get operation filtered to campaign_id c500-weekly-tip-001.", "labs/workflows/lab04-video-campaign-pipeline.json\nTable: c500_campaign_queue\nOperation: Row / Get"),
            ("Inspect Approval Gate. Only approval_status exactly approved reaches Pipeline Configuration and the persistent run query. Pending content routes to Record Unapproved Skip and stops before HeyGen or Telegram.", "pending -> skipped_unapproved\napproved -> validate snapshot -> query ledger"),
            ("Inspect Find Existing Run. It is a Data Table Row/Get operation on c500_campaign_runs filtered by request_key c500-video:<campaign_id>, limited to one row and configured to output an empty item when no row exists. Classify Existing Run routes an existing row to Record Duplicate Skip and a no-row result to Insert Run Ledger.", "request_key = c500-video:<campaign_id>\nexisting row -> skipped_duplicate\nno row -> Insert Run Ledger"),
            ("Run the pending row. Confirm Insert Run Ledger, Create Avatar Video and Publish Private Preview do not execute. Record skipped_unapproved and zero external calls.", "Expected external provider calls: 0\nExpected ledger inserts: 0"),
            ("Review the exact script, hash, profile version and private destination, then change only approval_status to approved. Open Pipeline Configuration and set authorised avatar_id, voice_id, profile_version c500-demo-1, poll_seconds 15 and maximum_poll_attempts 20.", "approval_status: approved\nprofile_version: c500-demo-1\nmaximum_poll_attempts: 20"),
            ("Inspect Validate Approved Snapshot and Hash Queue Script. The Code node checks required snapshot fields and profile version; the native n8n Crypto node writes SHA-256 into script_hash. Approved Snapshot Valid requires exact equality with approved_script_hash and a non-empty approved_destination_id. A mismatch stops before ledger insert and provider calls.", "Hash Queue Script: SHA256(approved_script) -> script_hash\nscript_hash = approved_script_hash\napproved_profile_version = configured profile_version"),
            ("Select HeyGen credentials in Create Avatar Video and Check Video Status. Confirm Insert Run Ledger writes request_key and status rendering before Create, and Store Provider Video ID updates that same row immediately after a successful create response.", "insert status: rendering\ncreate calls: at most 1\nupdate video_id: before Wait"),
            ("Inspect error wiring. Create and status HTTP error outputs, failed state, timeout and failed Release Checks all reach Mark Review Required, which updates the same request_key with status review_required, error_class and the known video_id when available.", "error -> review_required\nknown video_id retained\nnever route error to Create"),
            ("Inspect Wait, Check Video Status and Route Status. Processing increments attempts and loops to Wait; completed goes to Release Checks; failed or attempt 20 goes to Mark Review Required. No loop returns to Create Avatar Video.", "processing -> Wait\ncompleted -> Release Checks\nfailed|timeout -> Mark Review Required"),
            ("Inspect Hash Release Script and Release Checks. The native Crypto node recomputes the script hash; Release Checks requires completed status, non-empty video_url, exact hash and profile matches, then passes through only the trusted approved_destination_id from the queue snapshot. No provider or publish response may replace that destination.", "Required: completed + video_url + exact hash + exact profile\nPublish destination source: approved queue snapshot only"),
            ("Open Publish Private Preview. Select the Telegram credential, Send Video by URL, Chat ID from approved_destination_id and a caption that includes synthetic-media disclosure. Its error output must also reach Mark Review Required.", "Video: {{$json.video_url}}\nChat ID: {{$json.approved_destination_id}}\nCaption suffix: Generated with an AI avatar - training preview."),
            ("Inspect Mark Published. It updates the existing c500_campaign_runs row filtered by request_key with status published, video ID and URL, Telegram message ID, attempts, exact hash, profile version and completed_at.", "Operation: Data Table Row / Update\nFilter: request_key\nstatus: published"),
            ("Run the approved row once. Observe one ledger insert, one create call, the known video ID through bounded polling, one private disclosed Telegram post and one published update.", "Expected ledger rows for request_key: 1\nExpected create calls: 1\nExpected Telegram posts: 1"),
            ("Replay with Manual Trigger. Confirm Find Existing Run returns the persisted row and Record Duplicate Skip executes; Insert Run Ledger, HeyGen and Telegram must not execute. Save the execution trace.", "Expected: skipped_duplicate\nAdditional create calls: 0\nAdditional Telegram posts: 0"),
            ("Complete the runbook with owners, source and snapshot rules, schedule, maximum one video per run, poll deadline, monthly usage limit, monitoring, status-only recovery, credential rotation, retention, private-to-public review and rollback. Leave Schedule Trigger disabled. Save a node-by-node diff checklist naming only credential selectors, authorised IDs and Data Table bindings changed from the starter.", "Recovery: labs/workflows/lab03-status-resume.json\nTimezone: Asia/Singapore\nExample schedule: Monday 09:00\nFinal schedule state: disabled\nDiff: tables + credentials + authorised IDs only"),
        ],
        test=(
            "Pending content causes zero ledger inserts and zero external calls. The exact approved snapshot inserts one persistent request key before one create call, stores the returned video ID, reaches published or review_required through bounded polling, and writes every error path to the ledger. "
            "A published run sends one disclosed private video, while replay resolves through the persistent existing-row query with zero additional render or Telegram calls. A known timed-out job can be checked through the status-only workflow without calling create."
        ),
        checkpoint=(
            "Leave Schedule Trigger disabled and retain the synthetic queue row, persistent run-ledger row, private preview, duplicate-skip trace and runbook. Rejoin here: import labs/workflows/lab04-video-campaign-pipeline.json, bind both Data Tables and credentials, set Pipeline Configuration, confirm approval snapshot hash, then run Manual Trigger; for any retained video_id use labs/workflows/lab03-status-resume.json and never rerun Create."
        ),
        troubleshooting=[
            ("A pending row reaches HeyGen", "Stop the run and confirm Approval Gate is before Validate Approved Snapshot, both existence checks, ledger insert and every external provider node."),
            ("A replay creates another video", "Disable the workflow, confirm request_key is identical, bind both Data Table existence operations to c500_campaign_runs and restore the rowNotExists/rowExists branches before Create."),
            ("Ledger remains rendering after a provider error", "Connect the HTTP error output to Mark Review Required and update the same request_key with error_class plus any known video_id."),
            ("Telegram cannot send the video URL", "Keep the run ledger, mark review_required, verify bot access and approved_destination_id, then retry only the publish stage after human review; never create another video."),
        ],
        challenge="Add an approval-expiry timestamp to the trusted queue snapshot and prove an expired row fails before ledger insert, HeyGen or Telegram.",
        reflection="What production database constraint would make the persistent request_key guarantee atomic when two scheduler executions start at the same instant?",
    ),
]

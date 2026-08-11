# C500 Browser Apps

- `voice-console/` records one short microphone clip and sends multipart binary field `data` to the Lab 1 webhook.
- `video-studio/` first requests a synthetic HarbourStay draft, preserves its exact script, disclosure and SHA-256 hash for review, then sends that unchanged approval snapshot to the Lab 3 render path.

Serve an app locally so microphone and browser storage behave consistently:

```text
python -m http.server 8000 --directory labs/apps/voice-console
python -m http.server 8001 --directory labs/apps/video-studio
```

On Windows, use `py -m http.server ...` if the `python` command is not on PATH.

The apps store only the webhook URL in the current browser. They never request or store provider keys.

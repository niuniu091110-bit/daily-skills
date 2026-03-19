# Deployment Guide

## FastAPI Server

```python
# webhook_server.py
from fastapi import FastAPI, Request, HTTPException, Header
from webhook_handler import WebhookHandler, EventRouter, verify_github_signature
import os

app = FastAPI()
handler = WebhookHandler(secret=os.environ["WEBHOOK_SECRET"])
router = EventRouter()

@router.route("push", "pull_request")
async def handle_git(event):
    print(f"Received: {event.event_type} on {event.repo}")

@router.route("issue_comment")
async def handle_comment(event):
    print(f"Comment on #{event.raw_payload['issue']['number']}")

handler.use(router)

@app.post("/webhook")
async def webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None),
):
    body = await request.body()
    headers = {
        "X-GitHub-Event": x_github_event,
        "X-Hub-Signature-256": x_hub_signature_256,
    }
    try:
        await handler.handle(body, x_hub_signature_256, headers)
        return {"status": "ok"}
    except PermissionError:
        raise HTTPException(status_code=403, detail="Invalid signature")
```

## Running

```bash
uvicorn webhook_server:app --host 0.0.0.0 --port 8000
```

## Nginx Config (HTTPS)

```nginx
server {
    listen 443 ssl;
    server_name webhook.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location /webhook {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `WEBHOOK_SECRET` | GitHub/Stripe webhook secret |
| `STRIPE_WEBHOOK_SECRET` | Stripe-specific signing secret |
| `SLACK_SIGNING_SECRET` | Slack signing secret |

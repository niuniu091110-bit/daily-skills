# Event Formats Reference

## GitHub Events

### push
```json
{
  "ref": "refs/heads/main",
  "before": "abc123",
  "after": "def456",
  "repository": { "full_name": "owner/repo" },
  "pusher": { "name": "user", "email": "user@example.com" },
  "commits": [
    { "id": "abc", "message": "fix: bug", "author": { "name": "User" } }
  ]
}
```

### pull_request
```json
{
  "action": "opened|closed|merged",
  "number": 42,
  "pull_request": {
    "title": "feat: new feature",
    "state": "open",
    "merged": false,
    "user": { "login": "username" }
  },
  "repository": { "full_name": "owner/repo" }
}
```

### issue_comment
```json
{
  "action": "created|edited|deleted",
  "issue": { "number": 42, "title": "Bug report" },
  "comment": { "body": "This is a comment", "user": { "login": "user" } }
}
```

## Stripe Events

```json
{
  "id": "evt_xxx",
  "type": "payment_intent.succeeded",
  "created": 1677253600,
  "data": {
    "object": {
      "id": "pi_xxx",
      "amount": 2000,
      "currency": "usd",
      "status": "succeeded"
    }
  }
}
```

Common types:
- `payment_intent.succeeded`
- `payment_intent.payment_failed`
- `invoice.paid`
- `invoice.payment_failed`
- `customer.subscription.updated`

## Slack Events

```json
{
  "type": "event_callback",
  "token": "xxx",
  "team_id": "Txxx",
  "api_app_id": "Axxx",
  "event": {
    "type": "message.channels",
    "channel": "Cxxx",
    "user": "Uxxx",
    "text": "Hello!",
    "ts": "1677253600.123456"
  }
}
```

URL verification handshake:
```json
{ "type": "url_verification", "challenge": "xxx" }
```

# Signature Verification Reference

## GitHub Webhooks

GitHub uses HMAC-SHA256. The signature is in `X-Hub-Signature-256` header.

```
HMAC-SHA256(secret, raw_body) -> "sha256=<hex_digest>"
```

```python
import hmac, hashlib

def verify_github(payload: bytes, sig: str, secret: str) -> bool:
    expected = "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig)
```

Headers to check:
- `X-Hub-Signature-256`: HMAC signature
- `X-GitHub-Event`: Event type (push, pull_request, etc.)
- `X-GitHub-Delivery`: Unique delivery ID

## Stripe Webhooks

Stripe uses a combination of timestamp + signature.

```
signature = "t=<timestamp>,v1=<signature>"
expected = HMAC-SHA256("v0", "<timestamp>.<payload>", secret)
```

```python
import hmac, hashlib, time

def verify_stripe(payload: bytes, sig: str, secret: str, tolerance: int = 300) -> bool:
    parts = dict(p.split("=", 1) for p in sig.split(","))
    ts = int(parts["t"])
    if abs(time.time() - ts) > tolerance:
        return False  # replay attack protection
    msg = f"{ts}.".encode() + payload
    expected = hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, parts["v1"])
```

## Slack Webhooks

```
basestring = "v0:{timestamp}:{body}"
signature = "v0=" + HMAC-SHA256(basestring, signing_secret)
```

```python
import hmac, time

def verify_slack(body: str, timestamp: str, sig: str, secret: str) -> bool:
    if abs(time.time() - int(timestamp)) > 300:
        return False
    base = f"v0:{timestamp}:{body}"
    expected = "v0=" + hmac.new(secret.encode(), base.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig)
```

## Common Mistakes

1. **Raw body**: Always verify against the raw bytes, not parsed JSON
2. **Timing attack**: Always use `hmac.compare_digest` (constant-time comparison)
3. **Replay attacks**: Check timestamp for Stripe and Slack
4. **Encoding**: Use UTF-8 bytes for the payload

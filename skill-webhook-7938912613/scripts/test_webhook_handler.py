#!/usr/bin/env python3
"""Test webhook handler functionality."""

import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))

from webhook_handler import (
    verify_github_signature, verify_slack_signature,
    WebhookHandler, EventRouter, WebhookEvent
)
import hashlib, hmac, time

def test_github_signature():
    secret = "test-secret"
    payload = b'{"action":"push","repo":"test/repo"}'
    sig = "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    assert verify_github_signature(payload, sig, secret), "GitHub signature should verify"
    assert not verify_github_signature(payload, "sha256=bad", secret), "Bad sig should fail"
    print("[OK] GitHub signature verification")

def test_slack_signature():
    secret = "test-slack-secret"
    timestamp = str(int(time.time()))
    body = '{"type":"message"}'
    base = f"v0:{timestamp}:{body}"
    sig = "v0=" + hmac.new(secret.encode(), base.encode(), hashlib.sha256).hexdigest()
    assert verify_slack_signature(secret, timestamp, body, sig), "Slack sig should verify"
    print("[OK] Slack signature verification")

def test_event_router():
    router = EventRouter()
    results = []

    @router.route("push", "pull_request")
    def handle_git(e):
        results.append(("git", e.event_type))

    @router.route("payment")
    def handle_payment(e):
        results.append(("payment", e.event_type))

    e1 = WebhookEvent(raw_payload={}, event_type="push", headers={})
    e2 = WebhookEvent(raw_payload={}, event_type="payment", headers={})

    router.dispatch("push", e1)
    router.dispatch("payment", e2)
    router.dispatch("unknown", WebhookEvent(raw_payload={}, event_type="unknown", headers={}))

    assert ("git", "push") in results
    assert ("payment", "payment") in results
    assert len([r for r in results if r[0] == "git" and r[1] == "push"]) == 1
    print("[OK] Event router")

def test_webhook_handler():
    secret = "handler-test"
    handler = WebhookHandler(secret=secret)
    router = EventRouter()
    handled = []

    @router.route("push")
    def handle_push(e):
        handled.append(e.event_type)

    handler.use(router)
    payload = json.dumps({"action": "push"}).encode()
    sig = "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    headers = {"X-GitHub-Event": "push"}

    import asyncio
    asyncio.run(handler.handle(payload, sig, headers))
    assert "push" in handled
    print("[OK] WebhookHandler integration")

if __name__ == "__main__":
    test_github_signature()
    test_slack_signature()
    test_event_router()
    test_webhook_handler()
    print("\nAll tests passed!")

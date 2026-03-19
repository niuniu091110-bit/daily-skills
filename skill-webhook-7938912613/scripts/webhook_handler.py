#!/usr/bin/env python3
"""
Webhook Handler - Core library for processing webhooks
"""

import hashlib
import hmac
import json
import time
import asyncio
from typing import Callable, Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventRouter:
    """Routes webhook events to registered handlers based on event type."""

    def __init__(self):
        self._routes: Dict[str, List[Callable]] = defaultdict(list)

    def route(self, *event_types: str) -> Callable:
        """Decorator to register a handler for one or more event types."""
        def decorator(func: Callable) -> Callable:
            for et in event_types:
                self._routes[et].append(func)
            return func
        return decorator

    def dispatch(self, event_type: str, event: 'WebhookEvent') -> List[Any]:
        """Dispatch an event to all registered handlers."""
        results = []
        for handler in self._routes.get(event_type, []):
            try:
                result = handler(event)
                results.append(result)
            except Exception as e:
                logger.error(f"Handler error for {event_type}: {e}")
        return results


@dataclass
class WebhookEvent:
    """Parsed webhook event."""
    raw_payload: dict
    event_type: str
    headers: dict
    timestamp: float = field(default_factory=time.time)
    retry_count: int = 0

    @property
    def action(self) -> Optional[str]:
        return self.raw_payload.get("action")

    @property
    def repo(self) -> Optional[str]:
        return self.raw_payload.get("repository", {}).get("full_name")


class RetryQueue:
    """In-memory retry queue with exponential backoff."""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self._queue: Dict[str, List['WebhookEvent']] = defaultdict(list)
        self._processed: set = set()

    def enqueue(self, event: WebhookEvent, handler: Callable):
        """Add event to retry queue."""
        if event.retry_count >= self.max_retries:
            logger.warning(f"Event {event.event_type} exceeded max retries, moving to DLQ")
            self._move_to_dlq(event)
            return

        delay = self.base_delay * (2 ** event.retry_count)
        asyncio.create_task(self._delayed_process(event, handler, delay))

    async def _delayed_process(self, event: WebhookEvent, handler: Callable, delay: float):
        await asyncio.sleep(delay)
        try:
            handler(event)
            logger.info(f"Retry succeeded for {event.event_type}")
        except Exception as e:
            logger.error(f"Retry failed: {e}")
            event.retry_count += 1
            self.enqueue(event, handler)

    def _move_to_dlq(self, event: WebhookEvent):
        """Move to dead letter queue."""
        logger.error(f"DLQ: {event.event_type} - {json.dumps(event.raw_payload)[:200]}")


# --- Signature Verification ---

def verify_github_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify GitHub webhook HMAC-SHA256 signature."""
    if not signature.startswith("sha256="):
        return False
    expected = "sha256=" + hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def verify_stripe_signature(payload: bytes, signature: str, secret: str, tolerance: int = 300) -> bool:
    """Verify Stripe webhook signature with timestamp validation."""
    try:
        parts = dict(item.split("=") for item in signature.split(","))
        timestamp = parts.get("t", "")
        v1 = parts.get("v1", "")
        expected = hmac.new(secret.encode(), f"{timestamp}.".encode() + payload, hashlib.sha256).hexdigest()
        if hmac.compare_digest(expected, v1):
            # Check timestamp tolerance
            if abs(int(timestamp) - time.time()) <= tolerance:
                return True
        return False
    except Exception:
        return False


def verify_slack_signature(signing_secret: str, timestamp: str, body: str, signature: str) -> bool:
    """Verify Slack request signature."""
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False
    base = f"v0:{timestamp}:{body}"
    expected = "v0=" + hmac.new(signing_secret.encode(), base.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


# --- Main Handler ---

class WebhookHandler:
    """Main webhook handler with router and retry support."""

    def __init__(self, secret: str, verify_fn: Optional[Callable] = None):
        self.secret = secret
        self.verify_fn = verify_fn or (lambda p, s: verify_github_signature(p, s, secret))
        self.router = EventRouter()
        self.retry_queue = RetryQueue()

    def use(self, router: EventRouter):
        self.router = router

    def parse(self, payload_bytes: bytes, headers: dict, raw_body: str) -> Optional[WebhookEvent]:
        """Parse raw webhook into a WebhookEvent."""
        try:
            payload = json.loads(payload_bytes)
            event_type = headers.get("X-GitHub-Event", headers.get("Slack-Callback-Request", "unknown"))
            return WebhookEvent(raw_payload=payload, event_type=event_type, headers=headers)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse payload: {e}")
            return None

    async def handle(self, payload_bytes: bytes, signature: str, headers: dict):
        """Handle incoming webhook request."""
        if not self.verify_fn(payload_bytes, signature):
            raise PermissionError("Invalid signature")

        event = self.parse(payload_bytes, headers, payload_bytes.decode())
        if event is None:
            return

        results = self.router.dispatch(event.event_type, event)
        if not results:
            logger.warning(f"No handler for event type: {event.event_type}")
        return results

---
name: webhook-event-handler
description: 处理第三方 webhook 事件（GitHub、Stripe、Slack 等）的完整工作流。支持：签名验证（HMAC-SHA256）、事件解析与路由、自动重试与死信队列、日志与监控。当收到 webhook 推送、配置 webhook 处理服务、验证 webhook 真实性、处理支付/代码提交/聊天事件时使用。
---

# Webhook Event Handler

处理来自第三方服务的 webhook 事件，提供统一的签名验证、事件路由和重试机制。

## 快速开始

```python
from webhook_handler import WebhookHandler, EventRouter

handler = WebhookHandler(secret=os.environ["WEBHOOK_SECRET"])
router = EventRouter()

@router.route("push", "pull_request")
async def handle_git_event(event):
    print(f"Git event: {event.action} on {event.repo}")

handler.use(router)
await handler.run()  # 启动 HTTP 服务器
```

## 核心组件

### 1. 签名验证

```python
from webhook_handler import verify_signature

# HMAC-SHA256 验证（GitHub、Slack 等）
def verify_github_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = "sha256=" + hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

### 2. 事件路由

```python
from webhook_handler import EventRouter

router = EventRouter()

# 路由到多个处理函数
router.route("push", "pull_request", "issue_comment")
def handle_github(event):
    ...

# Stripe 事件
router.route("payment_intent.succeeded", "invoice.paid")
def handle_payment(event):
    ...

# Slack 事件
router.route("message.channels", "reaction_added")
def handle_slack(event):
    ...
```

### 3. 重试与死信队列

```python
from webhook_handler import RetryQueue

queue = RetryQueue(max_retries=3, backoff="exponential")
queue.enqueue(event, handler=my_handler)
```

## 详细参考

- **签名验证细节**: See [references/signature-verification.md](references/signature-verification.md)
- **事件格式参考**: See [references/event-formats.md](references/event-formats.md)
- **部署指南**: See [references/deployment.md](references/deployment.md)

## 部署

推荐使用 FastAPI + Uvicorn：

```bash
uvicorn webhook_server:app --host 0.0.0.0 --port 8000
```

生产环境建议配合 Nginx 反向代理和 HTTPS。

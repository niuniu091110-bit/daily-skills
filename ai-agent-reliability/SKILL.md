---
name: ai-agent-reliability
description: Diagnose, fix, and prevent AI agent failures in production. Use when an AI agent is behaving unreliably, failing unexpectedly, producing inconsistent outputs, or when planning a production-ready AI agent deployment. Triggers on: "AI agent keeps failing", "agent unreliable", "why did my agent fail", "agent error", "agent hallucination", "agent loop", "autonomous agent problems", "production AI agent checklist", "agent recovery".
---

# AI Agent Reliability

诊断和修复 AI agent 生产故障的框架。76% 的 AI agent 部署在 2026 年失败——大多数是可预防的。

## 核心原则

1. **越小越好** — agent 做越少的事，可靠性越高
2. **人类在环** — 关键决策需要 human-in-the-loop
3. **验证一切** — 不要假设 agent 的输出正确
4. **优雅降级** — agent 失败时要有 fallback

## 诊断框架：FAIL 检查

遇到 agent 故障时，按顺序检查：

### 🔍 Failure Mode Identification（故障模式识别）

```
常见故障模式：
1. Loop（循环）— agent 重复同一动作
   症状：API 调用重复、文件重复写入、相同问题反复问用户
   原因：缺少停止条件、反馈信号不清晰

2. Hallucination（幻觉）— agent 自信地输出错误信息
   症状：引用不存在的文件/函数、编造 API 响应
   原因：工具描述不完整、缺少验证

3. Drift（漂移）— agent 偏离原始目标
   症状：最终结果和需求无关、超出scope
   原因：目标定义不清晰、缺少中间检查点

4. Timeout（超时）— agent 卡住或无限等待
   症状：请求无响应、进程挂起
   原因：外部服务慢、缺少超时设置、死锁

5. Permission（权限）— agent 无法执行必要操作
   症状：Permission denied、认证失败
   原因：token/key 缺失、scope 不够
```

### ✅ Action Verification（动作验证）

每个 agent 动作后必须验证：
- 文件真的写入了吗？
- API 调用真的成功了吗？（检查 status code）
- 返回的数据格式符合预期吗？

### 💾 Intermediate State Persistence（中间状态持久化）

Agent 长时间任务必须定期保存状态：
- Checkpoint：每个关键步骤后保存进度
- Recovery：失败后从 checkpoint 恢复而不是从头开始

### 🔗 Loop Prevention（循环预防）

添加循环检测：
```javascript
// 伪代码：防止重复动作
const seen = new Set();
if (seen.has(actionKey)) {
  throw new Error("Loop detected, aborting");
}
seen.add(actionKey);
```

## 快速检查清单：部署前必做

```
□ Agent 的工具描述完整吗？（无歧义、有示例）
□ 每个工具调用有超时设置吗？
□ 关键操作有 human-in-the-loop 吗？
□ Agent 输出有验证步骤吗？
□ 失败时有清晰的错误消息吗？
□ 有 fallback 方案吗？
□ 日志记录完整吗？
□ Checkpoint 保存机制有吗？
```

## Recovery 策略

### 策略 1：重试 + 指数退避
```javascript
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === maxRetries - 1) throw e;
      await sleep(Math.pow(2, i) * 1000);
    }
  }
}
```

### 策略 2：降级到简单路径
```javascript
async function agentTask() {
  try {
    // 尝试完整路径
    return await complexAgentFlow();
  } catch {
    // 降级到简单路径
    return await simpleFallback();
  }
}
```

### 策略 3：分段执行 + 检查点
```
Step 1: Plan → Save checkpoint
Step 2: Execute subtask 1 → Verify → Save checkpoint
Step 3: Execute subtask 2 → Verify → Save checkpoint
...
Step N: Finalize → Save checkpoint
```

## Hallucination 对策

1. **工具描述必须具体**：包含参数类型、示例返回值、错误情况
2. **输出 schema 验证**：用 JSON Schema 验证 agent 输出
3. **交叉验证**：用另一个 agent 或规则检查第一个 agent 的输出
4. **不确定性表达**：要求 agent 在不确定时输出 `UNSURE` 而不是猜测

## 常见陷阱

| 陷阱 | 为什么失败 | 解法 |
|------|-----------|------|
| 单一巨大 prompt | 上下文稀释、指令忽略 | 拆分成多个小 agent |
| 无验证的链式调用 | 错误累积放大 | 每步验证 |
| 假设外部系统可靠 | 网络/API 不稳定 | 超时 + 重试 + fallback |
| 缺少权限边界 | 安全问题和权限错误 | 明确列出所需权限 |
| 没有错误预算 | 小问题升级成大故障 | 限制重试次数和总执行时间 |

## 何时扩大 scope

只有当以下都满足时才让 agent 做更多：
- 当前任务 10 次连续成功
- 所有边界情况都有处理
- 有完整的日志和监控
- 人类能理解 agent 的决策过程

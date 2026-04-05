# AI Context Overflow Handler

## Overview
诊断并解决 AI Agent 的 Context Overflow（上下文溢出）问题——当对话历史、系统提示、RAG 检索消耗完 context window 后，AI 开始"失忆"、循环、产生幻觉的现象。提供 5 种生产级解决方案，让长程 Agent 稳定运行。

**适用场景**：多轮对话失控、Agent 执行长任务时性能下降、RAG 效果不稳定、token 费用暴涨。

## 触发词
- "上下文溢出了"
- "AI 开始重复说话了"
- "context window 满了"
- "AI 失忆了"
- "LLM 幻觉变严重了"
- "token 消耗太快"
- "context overflow"
- "AI 开始循环了"
- "long context 优化"

## 诊断：你的 Agent 中招了吗？

回答以下 3 个问题：
1. **对话超过 30 轮后 AI 质量明显下降？**
2. **长任务执行到一半开始出现重复指令？**
3. **Token 账单月环比增长 > 40% 但任务复杂度没变？**

→ 3 个全中 = 严重 Context Overflow
→ 2 个中 = 中度，需要干预
→ 1 个中 = 轻度，可观察

## 为什么 Context Overflow 发生

```
Context Window 消耗来源（按占比）：

┌─────────────────────────────────────────────────────┐
│ System Prompt        ████░░░░░░░░░░░░░  15-30%      │
│ Conversation History ████████████████░░  40-60%     │
│ RAG Retrieval Results ████████░░░░░░░░░  15-25%    │
│ Tool Response        ████░░░░░░░░░░░░░  5-15%      │
└─────────────────────────────────────────────────────┘

临界点：消耗超过 80% 后，模型开始严重降权早期信息
```

## 五大解决方案

### 方案 A: Memory Pointer 架构（即时有效）

**核心思想**：不塞原始数据，塞指针（references）。

```
传统方式（溢出）：
  [用户: xxx] [AI: yyy] [用户: zzz] ... → context window 爆炸

Memory Pointer 方式（稳定）：
  [用户: 最新请求] + [Pointer: 参考 memory#123, memory#456]
  → context window 稳定在固定大小
```

**实现代码（Mem0 示例）：**
```javascript
import { Mem0Client } from "mem0ai";

// 不塞历史对话 → 存成语义记忆
await client.add(
  "用户在做一个 React 项目，使用 TypeScript，偏好函数式组件",
  { user_id: "lly", category: "project_context" }
);

// 检索相关记忆，构建精简 context
const relevantMemories = await client.search(
  currentTask,
  { user_id: "lly", top_n: 5, category: "project_context" }
);

const compactContext = relevantMemories.map(m => m.text).join("\n");
// compactContext 永远 < 4K tokens
```

### 方案 B: Semantic Compression（即时有效）

**核心思想**：定期把旧对话压缩成摘要，释放 token 空间。

```
对话流：
  [轮次 1-50 原始对话]
    ↓ 每 20 轮触发压缩
  [轮次 1-20 摘要: 用户在调 API，项目是电商后端]
  [轮次 21-50 原始对话]
    ↓ 继续压缩
  [综合摘要: 电商后端开发中，完成了订单模块]
  [轮次 31-50 原始对话]
```

**压缩 Prompt 模板：**
```
请将以下对话历史压缩为 200 字以内的摘要，保留：
1. 关键决策和结论
2. 未解决的重要问题
3. 用户偏好和上下文

---对话历史---
{history}
---摘要---
```

### 方案 C: Redis 滑动窗口缓存（生产级）

**核心思想**：用 Redis 维护对话状态，context 只保留最近 N 条。

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Redis      │ ←── │  Session    │ ──→ │  AI Model   │
│  (全量历史)  │     │  Context    │     │  (只读窗口)  │
└─────────────┘     └─────────────┘     └─────────────┘
     ↑                     ↓
     │               ZADD session:{id}
     │               ZRANGE session:{id} -100 0
     │               (只取最近 100 条)
     ↓
  语义压缩后
  归档到向量库
```

**Redis 配置：**
```javascript
// 对话窗口（固定大小）
await redis.zadd(`session:${sessionId}`, {
  score: Date.now(),
  member: JSON.stringify({ role, content, tokens })
});
// 只保留最近 100 条
await redis.zremrangebyrank(`session:${sessionId}`, 0, -101);

// 语义归档（超过 500 条时触发）
const oldMessages = await redis.zrange(`session:${sessionId}`, 0, -200);
const summary = await compressWithLLM(oldMessages);
await vectorStore.add({ text: summary, sessionId });
```

### 方案 D: RAG 检索优化（中期有效）

**Context Overflow 的 RAG 陷阱：**
- 检索 Top-K 太多 → 淹没真正相关的内容
- 检索结果超过 context 50% → 挤压对话空间
- 相似度阈值过低 → 引入噪音导致幻觉

**优化方案：**
```javascript
// 原始（差）：Top-20 检索结果全塞进去
const rawResults = await vectorDB.search(query, { topK: 20 });

// 优化后：分层检索 + 重排序
const candidateResults = await vectorDB.search(query, { topK: 50 });
const reranked = await reranker.rerank(candidateResults, { topK: 5 });
// 只取 5 条高质量结果，总 token 减少 75%
```

**检索质量检查清单：**
- [ ] 每条检索结果的相似度分数 >= 0.75？
- [ ] 检索结果总 token 数 < context 的 30%？
- [ ] 检索内容和当前问题相关性 > 80%？

### 方案 E: Hybrid Window（长期架构）

**核心思想**：动态分配 context 空间给不同类型内容。

```
┌────────────────────────────────────────────────────────┐
│ Fixed Budget Context (e.g., 32K total)                 │
├──────────────────┬───────────────────┬────────────────┤
│ System + Task    │  Recent History   │  RAG Results   │
│ (4K tokens)      │  (16K tokens)      │  (12K tokens)  │
│ 固定不变          │  滑动窗口          │  动态调整       │
└──────────────────┴───────────────────┴────────────────┘

策略：
- System prompt: 写死，不允许增长
- Recent history: 保留最近 20 轮，自动压缩更早的
- RAG results: 按任务类型动态分配（代码任务 6K，设计任务 12K）
```

## Token 消耗监控

**每月必查：**
```javascript
// 计算当前 session 的 token 消耗
const estimateTokens = (messages) =>
  messages.reduce((sum, m) => sum + Math.ceil((m.content.length + m.role.length) / 4), 0);

// 阈值告警
if (currentTokens > maxTokens * 0.8) {
  console.warn("⚠️ Context 使用率超过 80%，触发压缩流程");
  await compressSession(sessionId);
}
```

**快速检查清单：**
- [ ] 每个 session 的 context 使用率 <= 70%？
- [ ] Token 消耗月环比波动 < 20%？（否则可能有泄漏）
- [ ] 存在 session 超过 50 轮还在用原始历史？

## 复盘模板

```
## Context Overflow 复盘 — {日期}

**现象**: [描述发生了什么]
**触发轮次**: [第几轮开始出问题]
**根因**: [是什么导致了溢出]
**方案**: [用了哪个方案解决]
**效果**: [Token 减少 % / 性能恢复情况]
```

## 常见踩坑

1. **过度压缩**：把关键决策也压缩掉 → Agent 重复犯错
   → 解决：建立"不可压缩"清单（决策、约束、偏好）

2. **RAG 地狱**：检索结果噪音太多 → 幻觉加重
   → 解决：先做 Query Expansion，再检索

3. **没有监控**：到账单出来才发现 token 暴涨
   → 解决：每 10 轮做一次 token 估算，超阈值告警

## 适用角色
- Backend Dev：实现 Redis/memory 存储层
- AI Engineer：设计 context 管理架构
- Tech Lead：制定团队 AI 使用规范
- DevOps：监控 token 成本

## Cost
- Mem0: 按 API 调用计费
- Redis: 云服务 ~$50/月（自托管免费）
- RAG 优化: 免费（算法改进）

## Limitations
- Memory Pointer 需要额外的检索调用，有 ~100ms 延迟
- 压缩会丢失一些细粒度信息
- 跨 session 的长期记忆需要额外的向量存储

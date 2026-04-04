# AI Agent Memory Management

## Overview
帮助AI Agent实现长期记忆与上下文管理，解决多轮对话中的"遗忘"问题。通过语义搜索和记忆框架，让Agent跨会话保持连续性。

## Triggers
- "AI agent 记不住上下文"
- "帮我管理Agent记忆"
- "长期记忆实现"
- "多轮对话记忆"
- "Agent memory management"

## 核心问题
AI Agent在长对话中容易"忘记"早期信息，导致：
- 重复询问用户已提供的信息
- 前后回答矛盾
- 无法建立长期用户偏好模型

## 解决方案框架

### 1. 记忆类型分层
| 类型 | 用途 | 存储方式 |
|------|------|----------|
| **短期记忆** | 当前会话上下文 | Working memory / KV store |
| **会话记忆** | 本次对话关键信息 | Message history |
| **长期记忆** | 跨会话知识/偏好 | Vector DB / Graph |

### 2. 推荐框架
- **Mem0**: 专为Agent设计的记忆层，支持语义搜索和个性化记忆
- **Letta**: 开放源码的Agent记忆服务器，支持有状态Agent
- **LangChain**: 通用的Agent开发框架，含Memory组件

### 3. LOCOMO Benchmark
2026年推出的长对话记忆评估标准，关键指标：
- 实时延迟 (latency)
- 成本效益 (cost-effectiveness)
- 长期信息保留率

## 实现步骤

### Step 1: 选择记忆框架
```javascript
// Mem0 示例
import { Mem0Client } from "mem0ai";
const client = new Mem0Client({ apiKey: "your-key" });

// 存储记忆
await client.add("用户喜欢简洁的回答风格", { user_id: "lly" });

// 检索记忆
const memories = await client.search("用户的沟通偏好", { user_id: "lly" });
```

### Step 2: 设计记忆Schema
定义需要记忆的实体：
- 用户偏好（语言风格、时区、常用工具）
- 项目上下文（当前任务、约束条件）
- 历史决策（关键选择及理由）

### Step 3: 记忆检索策略
```javascript
// 语义检索示例
const relevantMemories = await client.search(query, {
  user_id: userId,
  top_n: 5,
  filters: { type: "preference" }
});
```

## 决策点模板
遇到需要记忆的决策时：
```markdown
## [HH:MM] 记忆点 #N
**内容**: <需要记住的信息>
**类型**: preference | context | knowledge
**重要性**: 高/中/低
**有效期**: 永久/会话内/任务内
```

## 复盘检查清单
每次Agent任务后检查：
- [ ] 是否正确存储了关键信息？
- [ ] 检索时是否找到了相关记忆？
- [ ] 记忆是否影响了本次回答质量？

## 常见踩坑
1. **过度存储**: 什么都记 → 噪音过多，检索质量下降
2. **从不清理**: 记忆无限增长 → 检索变慢，存储成本上升
3. **语义漂移**: 同一概念用不同表述 → 检索命中率低

## Cost
框架使用成本：
- Mem0: 按API调用计费
- Letta: 开源免费，自托管
- LangChain: 开源免费

## Limitations
- 需要额外的API调用和存储
- 记忆质量依赖检索准确性
- 隐私敏感信息需要特殊处理

## Reference
- https://mem0.ai/blog/state-of-ai-agent-memory-2026
- https://machinelearningmastery.com/the-6-best-ai-agent-memory-frameworks-you-should-try-in-2026/

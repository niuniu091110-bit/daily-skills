# AI Productivity Paradox Handler

## Overview
诊断并解决 AI 开发工具的"速度幻觉"——团队感知快 24% 但实际慢 19% 的 productivity paradox。识别 18-Month Wall 风险，实施 outcome-based 度量体系，恢复真实生产力。

**适用场景**：团队引入 AI 编程工具后代码量上涨但交付速度没变、code review 积压严重、开发者感觉忙但产出不明。

## 触发词
- "AI 反而变慢了"
- "代码多了但交付没快"
- "感觉忙但不知道在忙什么"
- "AI 工具到底有没有用"
- "code review 积压"
- "18个月撞墙"
- "DORA指标恶化了"
- "AI 让团队更累"
- "AI productivity paradox"

## 诊断流程

### Step 1: 确认是否中招
回答以下 3 个问题：
1. **AI 生成代码接受率 < 50%？** （Copilot 只有 ~30% accepted）
2. **Code review 时间增加 > 30%？** （ bottleneck 迁移到了 review）
3. **代码 churn（变更频率）翻倍但 lead time 没变？**

→ 3 个全中 = 100% 中招
→ 2 个中 = 高风险
→ 1 个中 = 风险存在

### Step 2: 区分感知速度 vs 真实速度

| 维度 | AI 提升感知 | 真实情况 |
|------|------------|---------|
| 写代码速度 | ✅ 明显更快 | ⚠️ 只测了局部 |
| Code review 速度 | ❌ 变慢 | ✅ 这是真实瓶颈 |
| Lead time (commit→prod) | ❌ 没变化 | ✅ 这是真实产出 |
| Cognitive load | ✅ 降低 | ⚠️ 但产生新依赖 |
| 调试时间 | ❌ 增加 | ✅ 生成的代码更难调试 |

### Step 3: 计算你的 AI Net Score
```
AI Net Score = (AI 生成代码价值 - AI 生成代码代价) / 投入成本

价值 = 被接受的代码行数 × 接受率
代价 = review 时间增加 + 调试时间增加 + 维护负担

AI Net Score > 1.0 → 值得继续用
AI Net Score < 0.5 → 需要干预
AI Net Score < 0 → 纯浪费
```

## 干预方案

### 方案 A: 降低 AI 生成比例（立即有效）
- 把 AI 用途限制在：**样板代码、格式、翻译、单函数**
- 禁止 AI 生成：**业务逻辑、跨模块代码、安全相关、测试**
- 目标：接受率从 30% 提升到 60%+

### 方案 B: 重建 review 流程（中期）
```
1. AI 代码自动打标签：[AI-Generated] → reviewer 心理准备
2. AI 代码双 review：第一遍 AI 自审，第二遍人类 review
3. 差异 highlight：只看 AI 生成部分 vs 人工修改部分
4. 设立 AI code freeze 日：每周一天纯人工 review 积压
```

### 方案 C: 切换到 Outcome-Based 度量（长期）
**废弃指标（会被 AI 扭曲）：**
- 代码行数（AI 生成 10x）
- PR 数量（碎片化 PR 增加）
- Commit 频率（AI 导致过度提交）

**真实指标（AI 无法伪造）：**
- Lead Time：first commit → prod deploy（中位时间）
- Change Failure Rate：prod deploy 后 7 天内 revert/rollback 的比例
- MTTR：平均恢复时间
- Cycle Time：开始写代码 → merge 的时间（纯开发时间）
- Review Quality Score：post-merge bug 数量

### 方案 D: 18-Month Wall 预防
| 时间节点 | 预警信号 | 干预动作 |
|---------|---------|---------|
| 第 3 个月 | Review 队列开始积压 | 引人 or 限制 AI scope |
| 第 6 个月 | Bug rate 上升 | 强制 AI 代码双审 |
| 第 12 个月 | 开发者疲劳报告 | AI freeze day |
| 第 18 个月 | 产出不变但人员倦怠 | 全面流程审计 |

## 快速检查清单

**每次 Sprint 结束时检查：**
- [ ] Lead time 相比 3 个月前变了吗？（允许 ±10% 波动）
- [ ] Review 队列平均等待时间 < 4 小时？
- [ ] AI 代码接受率 >= 50%？
- [ ] Post-merge bug 没有增加？
- [ ] 开发者 self-reported fatigue score <= 6/10？

**任一未达成 → 进入干预流程**

## 适用角色
- Engineering Manager：看数据、做决策
- Tech Lead：设计 review 流程
- Senior Dev：帮团队识别 AI 陷阱
- CTO：制定 AI 使用策略

## Cost
免费（无需工具，纯流程改进）

## Limitations
- 需要至少 3 个月的历史数据才能做基准对比
- 18-Month Wall 预防需要管理层支持
- 小团队（< 5人）效果不明显，因为本身沟通成本低

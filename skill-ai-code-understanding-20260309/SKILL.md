---
name: ai-code-understanding
description: AI助手的代码语义理解能力提升工具。当用户遇到AI工具无法正确理解代码结构、上下文或业务逻辑时触发，如：(1) AI生成的代码不符合项目架构 (2) AI不理解模块间的依赖关系 (3) AI建议的修改破坏了现有功能 (4) AI对复杂业务逻辑的理解有误。本技能提供代码语义增强、上下文注入、架构约束和业务规则注入等解决方案，帮助AI更准确地理解和生成符合项目规范的代码。
---

# AI Code Understanding - 提升AI代码理解能力

## 核心问题

AI工具存在"语义盲"问题：
- 依赖grep和find，猜测代码边界
- 在无关文件中浪费context
- 缺乏对项目架构的整体理解
- 无法理解业务逻辑和约束

## 解决方案

### 1. 代码语义增强

在项目中添加语义注释，帮助AI理解代码意图：

```python
# 业务规则说明：
# 此函数处理订单金额计算，需满足以下约束：
# 1. 折扣码必须来自 whitelist 表
# 2. 会员等级决定折扣上限
# 3. 促销活动期间折扣叠加规则不同
def calculate_order_total(order, user):
    ...
```

### 2. 架构约束文件

创建 `.ai-context/architecture.md`：

```markdown
# 项目架构约束

## 模块依赖
- order-service → user-service: 仅通过RPC
- payment-service: 独立事务，不参与分布式事务
- notification: 异步，不阻塞主流程

## 数据库约定
- 禁止跨服务JOIN
- 所有表必须有 created_at, updated_at
- 软删除使用 deleted_at

## API规范
- RESTful风格
- 错误码统一在 errors.md
```

### 3. 上下文注入提示

当需要AI处理特定模块时，使用结构化上下文：

```
## 当前任务
修改订单模块的退款逻辑

## 重要约束
- 退款金额不能超过原订单实付金额
- 已发货订单需先退货才能退款
- 跨境支付有额外的风控检查

## 相关文件
- orders/models.py: Order, Refund 模型
- orders/services/refund.py: 退款核心逻辑
- orders/api/refund.py: 退款API端点
```

### 4. 业务规则文档

创建 `.ai-context/business-rules.md`：

```markdown
# 订单业务规则

## 退款规则
1. 未发货：全额退款
2. 已发货未收货：需退货，全额退款
3. 已收货：扣除运费后退款
4. 跨境：额外5工作日审核

## 折扣叠加
- 会员折扣 + 活动折扣：取最大值，不叠加
- 优惠券 + 满减：先满减后优惠券
```

## 快速使用

1. 在项目根目录创建 `.ai-context/` 文件夹
2. 添加 `architecture.md` 描述项目架构
3. 添加 `business-rules.md` 描述业务规则
4. 在代码中添加语义注释

## 适用场景

- AI生成的代码不符合项目规范
- AI不理解模块间的依赖关系
- AI的建议破坏了现有功能
- AI对业务逻辑的理解有误

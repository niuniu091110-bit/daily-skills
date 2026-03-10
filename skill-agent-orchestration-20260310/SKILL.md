---
name: agent-orchestration
description: Build and manage multi-agent AI systems with orchestration frameworks. Use when users want to coordinate multiple AI agents, build agent swarms, implement agent communication protocols, or create complex agent workflows. Covers agent discovery, task decomposition, parallel execution, result aggregation, and fault tolerance. Triggers on requests like "multi-agent system", "agent orchestration", "multiple AI agents working together", "agent swarm", "AI agent coordination", or "build agent team".
---

# Agent Orchestration System

## Overview

This skill enables AI agents to build and orchestrate multi-agent systems. As AI applications scale, single-agent systems reach limitations—orchestration frameworks solve this by coordinating multiple specialized agents to work together on complex tasks.

## Why Multi-Agent Systems?

- **Specialization**: Each agent can be optimized for specific tasks
- **Scalability**: Add more agents to handle increased workload
- **Resilience**: Failure of one agent doesn't crash the entire system
- **Parallelism**: Multiple agents can work simultaneously
- **Complexity**: Complex tasks can be decomposed into smaller, manageable pieces

## Architecture Patterns

### 1. Supervisor Pattern

A central agent coordinates sub-agents, delegates tasks, and aggregates results.

```
┌─────────────┐
│  Supervisor │
│    Agent    │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──┴──┐ ┌──┴──┐
│Sub 1│ │Sub 2│
└─────┘ └─────┘
```

**Use cases**: Task routing, hierarchical workflows, approval chains

### 2. Parallel Execution Pattern

Multiple agents process the same task simultaneously, results are aggregated.

```
         ┌─────┐
      ┌──│Agent│──┐
      │  └─────┘  │
   ┌──┴──┐     ┌──┴──┐
   │Agent│     │Agent│
   │  1  │     │  2  │
   └─────┘     └─────┘
         │
    ┌────┴────┐
    │Aggregator│
    └─────────┘
```

**Use cases**: Voting/ensemble, search across multiple sources, A/B testing

### 3. Sequential Pipeline

Agents pass results to the next agent in chain.

```
┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐
│Agent│──▶│Agent│──▶│Agent│──▶│Agent│
│  1  │   │  2  │   │  3  │   │  4  │
└─────┘   └─────┘   └─────┘   └─────┘
```

**Use cases**: Data pipelines, multi-step transformations, refinement chains

### 4. Debate/Consensus Pattern

Agents with different perspectives argue, then reach consensus.

```
    ┌──────┐
    │Judge │
    │Agent │
    └──┬───┘
  ┌────┴────┐
  │         │
┌─┴──┐   ┌─┴──┐
│Pro │   │Con │
│    │   │    │
└────┘   └────┘
```

**Use cases**: Decision making, conflict resolution, quality assurance

## Implementation Frameworks

### 1. LangChain Agents

```python
from langchain.agents import AgentExecutor, Tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

# Define tools for agents
tools = [
    Tool(name="search", func=search_fn, description="Search the web"),
    Tool(name="calculator", func=calculate_fn, description="Calculate math"),
]

# Create agent
agent = create_json_agent(llm, tools)

# Execute with orchestration
result = agent.run("Research and calculate ROI for AI implementation")
```

### 2. AutoGen (Microsoft)

```python
from autogen import ConversableAgent, AssistantAgent, UserProxyAgent

# Create agents
assistant = AssistantAgent("assistant", llm_config={"model": "gpt-4"})
user_proxy = UserProxyAgent("user_proxy")

# Define group chat for orchestration
group_chat = GroupChat(
    agents=[assistant, user_proxy],
    messages=[],
    max_round=10
)

# Run orchestration
manager = GroupChatManager(groupchat=group_chat)
result = user_proxy.initiate_chat(manager, message="Solve this problem")
```

### 3. CrewAI

```python
from crewai import Agent, Task, Crew

# Define agents with roles
researcher = Agent(
    role="Researcher",
    goal="Find accurate information",
    backstory="Expert researcher"
)

writer = Agent(
    role="Writer",
    goal="Create compelling content",
    backstory="Professional writer"
)

# Define tasks
research_task = Task(
    description="Research AI trends",
    agent=researcher
)

write_task = Task(
    description="Write article",
    agent=writer
)

# Create crew and execute
crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
result = crew.kickoff()
```

### 4. Custom Implementation

For specialized needs, build your own orchestration:

```python
class AgentOrchestrator:
    def __init__(self):
        self.agents = {}
        self.message_queue = asyncio.Queue()
        
    def register_agent(self, agent_id, agent_fn):
        self.agents[agent_id] = agent_fn
        
    async def dispatch(self, task, agent_ids):
        # Parallel execution
        tasks = [self.agents[aid](task) for aid in agent_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return self.aggregate(results)
    
    def aggregate(self, results):
        # Combine results based on strategy
        return combine_results(results)
```

## Communication Protocols

### Message Format

```python
from dataclasses import dataclass
from typing import Any, Optional
from enum import Enum

class MessageType(Enum):
    TASK = "task"
    RESULT = "result"
    ERROR = "error"
    HEARTBEAT = "heartbeat"

@dataclass
class AgentMessage:
    sender: str
    receiver: Optional[str]  # None for broadcast
    message_type: MessageType
    payload: Any
    correlation_id: str  # Track request across agents
    timestamp: float
```

### State Synchronization

```python
class SharedState:
    def __init__(self):
        self._state = {}
        self._lock = asyncio.Lock()
        
    async def update(self, key, value):
        async with self._lock:
            self._state[key] = value
            
    async def get(self, key):
        async with self._lock:
            return self._state.get(key)
```

## Task Decomposition

Break complex tasks into smaller, assignable pieces:

```python
def decompose_task(task: str) -> list[dict]:
    """Use LLM to break down task into subtasks"""
    prompt = f"""
    Break down this task into smaller, independent subtasks:
    {task}
    
    Return as JSON array:
    [{{"subtask": "...", "agent_type": "researcher|writer|analyst"}}]
    """
    # Call LLM to decompose
    return llm.call(prompt)
```

## Fault Tolerance

### Retry Strategy

```python
async def execute_with_retry(agent_fn, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await agent_fn()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### Fallback Agents

```python
async def execute_with_fallback(task, primary_agent, fallback_agent):
    try:
        return await primary_agent(task)
    except Exception as e:
        return await fallback_agent(task)
```

### Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failures = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "closed"
        
    def call(self, fn):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise CircuitOpenError()
        
        try:
            result = fn()
            self.state = "closed"
            self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = "open"
            raise
```

## Monitoring & Observability

### Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent-orchestration")

# Log agent activities
logger.info(f"Agent {agent_id} started task {task_id}")
logger.info(f"Agent {agent_id} completed task {task_id}, result: {result}")
```

### Metrics

```python
from prometheus_client import Counter, Histogram

task_counter = Counter('agent_tasks_total', 'Total tasks', ['agent_id', 'status'])
task_duration = Histogram('agent_task_duration', 'Task duration', ['agent_id'])

# Track metrics
task_counter.labels(agent_id=agent_id, status="success").inc()
task_duration.labels(agent_id=agent_id).observe(duration)
```

## Best Practices

1. **Start simple**: Begin with supervisor pattern, add complexity as needed
2. **Define clear interfaces**: Use structured message formats
3. **Implement timeouts**: Prevent agents from hanging indefinitely
4. **Add observability**: Log everything, metrics help with debugging
5. **Handle failures gracefully**: Circuit breakers, fallback agents
6. **Test thoroughly**: Multi-agent systems have emergent behaviors
7. **Consider cost**: Each agent call costs money, optimize orchestration

## Example Use Cases

| Use Case | Pattern | Framework |
|----------|---------|-----------|
| Research + Write article | Sequential | CrewAI |
| Code review by multiple agents | Parallel/Voting | Custom |
| Customer support triage | Supervisor | LangChain |
| Debate and decide | Consensus | Custom |
| Data extraction pipeline | Pipeline | LangChain |

## Decision Tree

```
Need multi-agent system?
├── Simple task routing → Supervisor pattern
├── Multiple perspectives → Debate/Consensus
├── Parallel processing → Parallel execution
├── Sequential steps → Pipeline
└── Complex, hierarchical → Combination of above
```

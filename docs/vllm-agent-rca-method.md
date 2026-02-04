# vLLM Agent RCA Method

This document explains the Root Cause Analysis (RCA) method implemented in the `vLLMAgent` class (`clients/vllm.py`).

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Component Breakdown](#component-breakdown)
  - [Agent Initialization](#1-agent-initialization)
  - [Context Initialization](#2-context-initialization)
  - [Action Loop](#3-action-loop)
  - [Main Execution Flow](#4-main-execution-flow)
- [RCA Loop Diagram](#rca-loop-diagram)
- [Example Conversation Flow](#example-conversation-flow)
- [Prompt Template](#prompt-template)
- [Configuration Parameters](#configuration-parameters)
- [Comparison with Other Clients](#comparison-with-other-clients)
- [Limitations](#limitations)

---

## Overview

The `vLLMAgent` is a **simple conversational agent** that uses a locally-hosted LLM (via vLLM server) to perform AIOps tasks:

- **Detection**: Is there an anomaly? (Yes/No)
- **Localization**: Which service(s) are faulty?
- **Analysis**: What is the system level and fault type?
- **Mitigation**: Fix the fault

The agent operates through an **iterative conversation loop** with the environment, using shell commands to investigate and a submit API to provide answers.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           AIOpsLab System                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐        │
│  │  vLLMAgent  │ ◄─────► │ Orchestrator│ ◄─────► │  Kubernetes │        │
│  │             │         │             │         │   Cluster   │        │
│  └─────────────┘         └─────────────┘         └─────────────┘        │
│         │                       │                                        │
│         │                       │                                        │
│         ▼                       ▼                                        │
│  ┌─────────────┐         ┌─────────────┐                                │
│  │ vLLM Server │         │  Problem    │                                │
│  │ (Local LLM) │         │  Registry   │                                │
│  └─────────────┘         └─────────────┘                                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Agent Initialization

**File**: `clients/vllm.py` (lines 12-29)

```python
class vLLMAgent:
    def __init__(
        self,
        model="openai/gpt-oss-20b",
        repetition_penalty=1.0,
        temperature=1.0,
        top_p=1.0,
        max_tokens=1024,
    ):
        self.history = []  # Conversation history

        self.llm = vLLMClient(
            model=model,
            repetition_penalty=repetition_penalty,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        )
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | str | `"openai/gpt-oss-20b"` | Model name on vLLM server |
| `repetition_penalty` | float | 1.0 | Penalize repeated tokens (1.0 = no penalty) |
| `temperature` | float | 1.0 | Controls randomness (higher = more random) |
| `top_p` | float | 1.0 | Nucleus sampling threshold |
| `max_tokens` | int | 1024 | Maximum tokens in response |

#### Key Attributes

| Attribute | Purpose |
|-----------|---------|
| `self.history` | Stores entire conversation for context (list of messages) |
| `self.llm` | vLLMClient instance for LLM inference |

---

### 2. Context Initialization

**File**: `clients/vllm.py` (lines 31-49)

```python
def init_context(self, problem_desc: str, instructions: str, apis: str):
    """Initialize the context for the agent."""

    # Step 1: Filter available APIs
    self.shell_api = self._filter_dict(apis, lambda k, _: "exec_shell" in k)
    self.submit_api = self._filter_dict(apis, lambda k, _: "submit" in k)

    # Step 2: Build system prompt
    def stringify_apis(apis):
        return "\n\n".join([f"{k}\n{v}" for k, v in apis.items()])

    self.system_message = DOCS_SHELL_ONLY.format(
        prob_desc=problem_desc,
        shell_api=stringify_apis(self.shell_api),
        submit_api=stringify_apis(self.submit_api),
    )

    self.task_message = instructions

    # Step 3: Initialize conversation history
    self.history.append({"role": "system", "content": self.system_message})
    self.history.append({"role": "user", "content": self.task_message})
```

#### What This Does

1. **Filters APIs**: Extracts only `exec_shell` and `submit` from available APIs
2. **Builds System Prompt**: Uses `DOCS_SHELL_ONLY` template with problem description
3. **Initializes History**: Sets up conversation with system message and task instructions

#### Input Parameters

| Parameter | Source | Content |
|-----------|--------|---------|
| `problem_desc` | Orchestrator | Task description (e.g., "You are an expert DevOps engineer...") |
| `instructions` | Orchestrator | How to respond (e.g., "Respond with Action: ...") |
| `apis` | Orchestrator | Dictionary of available API functions |

---

### 3. Action Loop

**File**: `clients/vllm.py` (lines 51-63)

```python
async def get_action(self, input) -> str:
    """Wrapper to interface the agent with OpsBench.

    Args:
        input (str): The input from the orchestrator/environment.

    Returns:
        str: The response from the agent.
    """
    self.history.append({"role": "user", "content": input})
    response = self.llm.run(self.history)
    self.history.append({"role": "assistant", "content": response[0]})
    return response[0]
```

#### How It Works

1. **Receive Input**: Environment result (e.g., command output) is added to history
2. **LLM Inference**: Entire conversation history is sent to LLM
3. **Get Response**: LLM generates next action
4. **Update History**: Response is added to history for context
5. **Return Action**: Action string returned to orchestrator

#### Conversation History Structure

```python
self.history = [
    {"role": "system", "content": "You are an expert DevOps engineer..."},
    {"role": "user", "content": "Instructions..."},
    {"role": "assistant", "content": "exec_shell('kubectl get pods')"},
    {"role": "user", "content": "NAME  STATUS  ...(command output)..."},
    {"role": "assistant", "content": "exec_shell('kubectl logs ...')"},
    # ... continues growing
]
```

---

### 4. Main Execution Flow

**File**: `clients/vllm.py` (lines 69-105)

```python
if __name__ == "__main__":
    # Optional: Enable Weights & Biases logging
    use_wandb = os.getenv("USE_WANDB", "false").lower() == "true"
    if use_wandb:
        wandb.init(project="AIOpsLab", entity="AIOpsLab")

    # Get all problem IDs from registry
    registry = ProblemRegistry()
    pids = registry.get_problem_ids()
    sample_pids = pids[:1]  # Run first problem only

    for pid in sample_pids:
        agent = vLLMAgent()  # Create new agent instance
        orchestrator = Orchestrator()
        orchestrator.register_agent(agent, name="gpt-oss-20b")

        try:
            # Initialize problem (deploy app, inject fault, start workload)
            problem_desc, instructs, apis = orchestrator.init_problem(pid)
            agent.init_context(problem_desc, instructs, apis)

            # Start the RCA loop (max 10 steps)
            asyncio.run(orchestrator.start_problem(max_steps=10))

        except Exception as e:
            print(f"Failed to process pid {pid}. Error: {e}")
            time.sleep(60)
            continue
```

#### Execution Steps

| Step | Action | Description |
|------|--------|-------------|
| 1 | Create Agent | Instantiate `vLLMAgent` with model config |
| 2 | Create Orchestrator | Set up problem orchestration |
| 3 | Register Agent | Link agent to orchestrator |
| 4 | Init Problem | Deploy app, inject fault, start workload |
| 5 | Init Context | Set up agent's system prompt |
| 6 | Start Problem | Begin RCA loop (max 10 iterations) |
| 7 | Evaluate | Check agent's answer against expected solution |

---

## RCA Loop Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           RCA LOOP                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   START                                                                  │
│     │                                                                    │
│     ▼                                                                    │
│   ┌─────────────────────────────────────────────────────────────┐       │
│   │  1. Agent receives environment state/command output          │       │
│   └─────────────────────────────────────────────────────────────┘       │
│     │                                                                    │
│     ▼                                                                    │
│   ┌─────────────────────────────────────────────────────────────┐       │
│   │  2. Agent appends input to conversation history              │       │
│   └─────────────────────────────────────────────────────────────┘       │
│     │                                                                    │
│     ▼                                                                    │
│   ┌─────────────────────────────────────────────────────────────┐       │
│   │  3. Full history sent to LLM for inference                   │       │
│   │     - System prompt (problem description, APIs)              │       │
│   │     - All previous turns (commands + outputs)                │       │
│   └─────────────────────────────────────────────────────────────┘       │
│     │                                                                    │
│     ▼                                                                    │
│   ┌─────────────────────────────────────────────────────────────┐       │
│   │  4. LLM generates next action                                │       │
│   │     - exec_shell("command") → Run shell command              │       │
│   │     - submit(solution) → Submit final answer                 │       │
│   └─────────────────────────────────────────────────────────────┘       │
│     │                                                                    │
│     ▼                                                                    │
│   ┌─────────────────────────────────────────────────────────────┐       │
│   │  5. Orchestrator parses and executes action                  │       │
│   └─────────────────────────────────────────────────────────────┘       │
│     │                                                                    │
│     ▼                                                                    │
│   ┌───────────────────────┐                                             │
│   │  Is action submit()?  │                                             │
│   └───────────────────────┘                                             │
│     │           │                                                        │
│    YES          NO                                                       │
│     │           │                                                        │
│     ▼           ▼                                                        │
│   ┌─────┐    ┌─────────────────────────────────────────┐                │
│   │ END │    │  Return command output as next input    │────► (Loop)    │
│   └─────┘    └─────────────────────────────────────────┘                │
│     │                                                                    │
│     ▼                                                                    │
│   ┌─────────────────────────────────────────────────────────────┐       │
│   │  6. Evaluate solution against expected answer                │       │
│   └─────────────────────────────────────────────────────────────┘       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Example Conversation Flow

### Detection Task: `pod_kill_hotel_res-detection-1`

| Turn | Role | Content |
|------|------|---------|
| 1 | **System** | "You are an expert DevOps engineer assigned to detect anomalies in a deployed service. Service Details: Hotel Reservation application running in namespace hotel-reserv..." |
| 2 | **User** | "You will begin by analyzing the service's state and telemetry, and then submit your solution: 'Yes' or 'No' to indicate whether there are anomalies detected." |
| 3 | **Assistant** | ```exec_shell("kubectl get pods -n hotel-reserv")``` |
| 4 | **User** | "NAME                    READY   STATUS             RESTARTS   AGE\nuser-6f8b9c7d5-x2k4p   0/1     CrashLoopBackOff   5          3m\nfrontend-7c9d8e6f4-m3n2  1/1     Running            0          10m\n..." |
| 5 | **Assistant** | ```exec_shell("kubectl describe pod user-6f8b9c7d5-x2k4p -n hotel-reserv")``` |
| 6 | **User** | "Events:\n  Warning  BackOff  pod/user-6f8b9c7d5-x2k4p  Back-off restarting failed container..." |
| 7 | **Assistant** | ```exec_shell("kubectl logs user-6f8b9c7d5-x2k4p -n hotel-reserv --previous")``` |
| 8 | **User** | "Error: Connection refused to mongodb-rate:27017..." |
| 9 | **Assistant** | ```submit("Yes")``` |
| 10 | **Orchestrator** | Evaluates: Expected "Yes" ✓ → **Success!** |

---

## Prompt Template

**File**: `clients/utils/templates.py`

```python
DOCS_SHELL_ONLY = """{prob_desc}
You are provided with a direct API to a secure terminal to the service where you can run commands:

{shell_api}

Finally, you will submit your solution for this task using the following API:

{submit_api}

IMPORTANT:
1. The submit() call must strictly follow its defined parameter signature for this task.
2. Provide the call in a markdown code block.

At each turn respond with:
Action: <your action>
"""
```

### Template Variables

| Variable | Content |
|----------|---------|
| `{prob_desc}` | Task-specific description (detection/localization/analysis/mitigation) |
| `{shell_api}` | `exec_shell(command: str) -> str` function signature and docs |
| `{submit_api}` | `submit(solution)` function signature (varies by task type) |

---

## Configuration Parameters

### vLLM Server Configuration

**File**: `clients/utils/llm.py` (line 261)

```python
client = OpenAI(api_key="EMPTY", base_url="http://10.201.135.228:8000/v1")
```

| Setting | Value |
|---------|-------|
| Server URL | `http://10.201.135.228:8000/v1` |
| API Key | `"EMPTY"` (not required for local vLLM) |

### LLM Inference Parameters

**File**: `clients/utils/llm.py` (lines 263-274)

```python
response = client.chat.completions.create(
    messages=payload,
    model=self.model,
    max_tokens=self.max_tokens,
    temperature=self.temperature,
    top_p=self.top_p,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    n=1,
    timeout=60,
    stop=[],
)
```

---

## Comparison with Other Clients

| Client | File | APIs Available | Reasoning Method | Use Case |
|--------|------|----------------|------------------|----------|
| **vLLM** | `vllm.py` | Shell only | Simple action | Local open-source models |
| **GPT** | `gpt.py` | Shell only | Simple action | OpenAI GPT models |
| **DeepSeek** | `deepseek.py` | Shell only | Simple action | DeepSeek models |
| **Qwen** | `qwen.py` | Shell only | Streaming | Alibaba Qwen models |
| **ReAct** | `react.py` | All APIs | Thought + Action | Structured reasoning |
| **FLASH** | `flash.py` | All APIs | Status supervision + hindsight | High reliability |
| **OpenRouter** | `openrouter.py` | Shell only | Simple action | Multiple model providers |

---

## Limitations

| Limitation | Description |
|------------|-------------|
| **No Telemetry APIs** | Cannot directly query Prometheus metrics, logs, or traces |
| **Growing Context** | Full history sent each turn (can hit context limits) |
| **No Explicit Reasoning** | Just "Action:" without "Thought:" chain-of-thought |
| **Single Agent** | No multi-agent collaboration |
| **No Memory Management** | No summarization or context compression |
| **Fixed Timeout** | 60-second timeout may be insufficient for slow models |

---

## Related Files

| File | Purpose |
|------|---------|
| `clients/vllm.py` | Main agent implementation |
| `clients/utils/llm.py` | LLM client (vLLMClient class) |
| `clients/utils/templates.py` | Prompt templates |
| `aiopslab/orchestrator/orchestrator.py` | Problem orchestration |
| `aiopslab/orchestrator/problems/registry.py` | Problem registry |
| `aiopslab/orchestrator/tasks/*.py` | Task definitions (detection, localization, etc.) |

---

## See Also

- [AIOpsLab Problem Registry](./problems.txt) - List of all available problems
- [Clients README](../clients/README.md) - Overview of all client implementations

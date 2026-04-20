# Smart Healthcare Orchestrator

This repository contains a lightweight, multi-agent orchestration framework built using an "Agent Development Kit" (ADK) pattern. It is designed to demonstrate how specialized AI agents can collaborate in a sequence to efficiently route medical complaints.

## Architecture Highlights

The application relies on a **Primary Orchestrator** to coordinate task flow between several specialized agent modules.

### ADK Core (`adk/`)
- **`Agent`**: An abstract base class out of which all specialized agents are constructed. It enforces a standard `execute()` lifecycle that processes inputs.
- **`Message`**: The fundamental communication contract. It acts as an envelope wrapping data across agents, ensuring payloads have explicitly tracked senders, receivers, and metadata.
- **`Orchestrator`**: A complex parent Agent that maintains a registry of sub-agents and uses `route_message()` to orchestrate logical sequences between them.

## The Triaging Flow

When a user provides unstructured text pertaining to a medical complaint, the orchestrator triggers the following pipeline:

1. **Symptom Agent**: Evaluates the unstructured conversational phrase (e.g., "My chest hurts and I'm sweating heavily") and transforms it into structured output data mapping recognizable keywords and symptom categories.
2. **Triage Agent**: Takes the structured array of symptoms, parses them against critical/moderate priority sets, and scores them. Depending on severity limits, it classifies the incident (High, Medium, Low).
3. **Routing Agent**: Consumes the triage classification output and enforces the final business logic to route the user. (e.g., Recommending ER vs. a typical clinical appointment).

## Getting Started

### Prerequisites
- Python 3.8+

### Installation & Execution
Clone the repository and run the primary orchestrator directly inside your terminal:
```bash
git clone https://github.com/arnabbhattacharjee1/Smart-Healthcare-Orchestrator.git
cd Smart-Healthcare-Orchestrator
python main.py
```

### Roadmap
Currently, text extraction relies on predefined heuristics / dummy mocks to convey the orchestration structure. Future enhancements will swap these out with true implementations using LLM APIs to perform robust zero-shot extraction.

# Architecture Documentation

## System Architecture

### Agent Maturity Level: Level 3 (Collaborative Multi-Agent System)

The ULB DPR Assistant implements a Level 3 multi-agent system with:
- **Level 0-1**: Individual agents with tools (Data Collection, Financial Modeling)
- **Level 2**: Strategic planning with context management (Orchestrator)
- **Level 3**: Multi-agent collaboration with shared memory and coordination

## Multi-Agent System Design

### Agent Hierarchy

```
Orchestrator Agent (Level 2-3)
├── Data Collection Agent (Level 1)
├── Financial Modeling Agent (Level 1)
├── Risk Assessment Agent (Level 1)
├── Document Generation Agent (Level 1)
└── Compliance Checker Agent (Level 1)
```

### Workflow

1. **Data Collection**: Gathers ULB-specific data (parallel where possible)
2. **Financial Modeling**: Creates financial projections with tariff affordability
3. **Risk Assessment**: Analyzes risks and historical failure patterns
4. **Document Generation**: Assembles DPR with sector-specific templates
5. **Compliance Check**: Validates against government standards
6. **Final Review**: Orchestrator coordinates final DPR assembly

## Key Components

### Services

- **Session Service**: Manages DPR creation sessions (InMemorySessionService)
- **Memory Service**: 
  - Episodic Memory: Past DPR attempts
  - Semantic Memory: Learned patterns
  - Working Memory: Active session context
- **Context Service**:
  - Token Budget Management
  - RAG for government guidelines
  - Selective Information Retrieval
- **Observability**:
  - Agent-specific logging
  - Distributed tracing
  - Metrics collection

### Tools

- **Sector Templates**: Water Supply, Solid Waste, Urban Transport, Streetlighting
- **Risk Mitigation**: Tariff affordability, political feasibility, public acceptance
- **Aggregation Intelligence**: ULB clustering recommendations
- **Platform Integrations**: HUDCO, Gati Shakti, SEBI, MoHUA

### State Configurations

- Chhattisgarh (primary focus)
- Template for other states
- State-specific PPP guidelines and successful cases

## Data Flow

```
User Input → Orchestrator → Data Collection
                              ↓
                         Financial Modeling
                              ↓
                         Risk Assessment
                              ↓
                         Document Generation
                              ↓
                         Compliance Check
                              ↓
                         Final DPR Output
```

## Evaluation Framework

### Metrics

1. **Bankability Score**: HUDCO/UiWIN compliance, Urban Challenge Fund readiness
2. **Replicability Index**: Adaptability to similar ULBs
3. **Risk Mitigation Effectiveness**: Avoids known failure patterns
4. **Aggregation Potential**: Clustering opportunities

## Technology Stack

- **Language**: Python 3.10+
- **Agent Framework**: Google ADK (Gemini)
- **RAG**: LangChain with Google Generative AI
- **Observability**: OpenTelemetry, Prometheus
- **Testing**: pytest, pytest-asyncio



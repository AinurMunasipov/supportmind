from dataclasses import dataclass


@dataclass
class AgentContextDecision:
    retrieve_memory: bool
    use_mcp: bool

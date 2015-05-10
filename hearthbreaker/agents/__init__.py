from hearthbreaker.agents.agent_registry import AgentRegistry as __ar__
from hearthbreaker.agents.basic_agents import RandomAgent
from hearthbreaker.agents.tempo_agent import TempoAgent
from hearthbreaker.agents.aggressive_agent import AggressiveAgent
from hearthbreaker.agents.control_agent import ControlAgent

registry = __ar__()

registry.register("Random", RandomAgent)
registry.register("Tempo", TempoAgent)
registry.register("Aggressive", AggressiveAgent)
registry.register("Control", ControlAgent)

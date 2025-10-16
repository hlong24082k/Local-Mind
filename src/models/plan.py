from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class PlanStep(BaseModel):
    """
    Represents one atomic action (tool invocation) in the plan.
    """
    tool: str = Field(..., description="Name of the tool to execute.")
    args: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the tool.")
    description: Optional[str] = Field(None, description="Short explanation of what this step does.")


class PlanResult(BaseModel):
    """
    A full multi-step plan for the agent to execute.
    """
    steps: List[PlanStep] = Field(default_factory=list, description="Ordered list of steps.")
    reasoning: Optional[str] = Field(None, description="LLM reasoning or context for the plan.")
    goal: Optional[str] = Field(None, description="User's original intent or task summary.")

    def add_step(self, step: PlanStep):
        self.steps.append(step)

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)

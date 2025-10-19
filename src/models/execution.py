from pydantic import BaseModel, Field
from src.models.tool import ToolResult


class ExecutionResult(BaseModel):
    step_results: list[ToolResult]

    def add(self, result: ToolResult):
        self.step_results.append(result)

    def summary(self) -> str:
        lines = []
        for i, r in enumerate(self.step_results, start=1):
            status = "✅" if r.success else "❌"
            lines.append(f"[{i}] {status} {r.message}")
        return "\n".join(lines)

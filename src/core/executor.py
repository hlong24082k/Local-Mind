from src.tools.tool_registry import ToolRegistry

from src.models.tool import ToolResult
from src.models.plan import PlanResult
from src.models.execution import ExecutionResult

class Executor:
    def __init__(self):
        self.tool_registry = ToolRegistry()

    def execute(self, plan: PlanResult) -> ExecutionResult:
        results = ExecutionResult(step_results=[])
        if not plan.steps:
            results.add(ToolResult(success=False, message='No steps to execute.'))

        for step in plan.steps:
            tool_def = self.tool_registry.get(step.tool)

            if not tool_def:
                results.add(ToolResult(success=False, message=f"Unknown tool: {step.tool}"))
                return results

            try:
                result = tool_def.func(**step.args)
                results.add(result)
            except Exception as e:
                results.add(ToolResult(success=False, message=f"Error executing {step.tool}: {e}"))

        return results
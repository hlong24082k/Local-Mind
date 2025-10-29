# src/core/validator.py
from src.models.plan import PlanResult
from src.models.validation import ValidationResult
from src.tools.tool_registry import ToolRegistry

class PlanValidator:
    """Validates if a Plan is structurally, logically, and semantically correct."""

    def __init__(self):
        self.tools = ToolRegistry()

    def validate(self, plan: PlanResult) -> ValidationResult:
        errors, warnings = [], []

        # 1. Structural validation
        if not plan.steps:
            errors.append("Plan contains no steps.")
            return ValidationResult(success=False, errors=errors)

        step_ids = set()
        for step in plan.steps:
            # Tool existence
            if step.tool not in self.tools.names():
                errors.append(f"Unknown tool: {step.tool}")

            # Args validation
            tool_def = self.tools.get(step.tool)
            if tool_def:
                missing = [p for p in tool_def.required_args if p not in step.args]
                if missing:
                    errors.append(f"Step '{step}' missing args: {missing}")

            # Safety validation
            if step.tool == "delete_file" and not step.args.get("confirm", False):
                warnings.append(f"Step '{step}' deletes file without confirmation.")

            # Dependency validation
            # for dep in step.depends_on or []:
            #     if dep not in step_ids:
            #         warnings.append(f"Step '{step}' depends on non-existent step: {dep}")

        success = len(errors) == 0
        return ValidationResult(success=success, errors=errors, warnings=warnings)

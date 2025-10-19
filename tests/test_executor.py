import pytest
from src.core.executor import Executor, ExecutionResult
from src.models.plan import PlanResult, PlanStep
from src.models.tool import ToolResult
from src.tools.tool_registry import ToolRegistry


# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture(autouse=True)
def reset_registry(monkeypatch):
    """
    Reset ToolRegistry between tests by mocking its internal _registry dict.
    """
    ToolRegistry._registry = {}  # clear all registered tools
    yield
    ToolRegistry._registry = {}  # cleanup after test


@pytest.fixture
def setup_mock_tools():
    """
    Register mock tools directly in the singleton registry.
    """
    def mock_success_tool(path):
        return ToolResult(success=True, message=f"Listed: {path}")

    def mock_fail_tool(path):
        return ToolResult(success=False, message=f"Failed: {path}")

    def mock_exception_tool(path):
        raise RuntimeError("Unexpected error")

    ToolRegistry.register("tool.success", mock_success_tool)
    ToolRegistry.register("tool.fail", mock_fail_tool)
    ToolRegistry.register("tool.exception", mock_exception_tool)


@pytest.fixture
def executor():
    return Executor(ToolRegistry)


# -----------------------------
# Tests
# -----------------------------
def test_execute_single_success(executor, setup_mock_tools):
    plan = PlanResult(steps=[
        PlanStep(tool="tool.success", args={"path": "./data"})
    ])

    result = executor.execute(plan)

    assert isinstance(result, ExecutionResult)
    assert len(result.step_results) == 1
    assert "Listed: ./data" in result.step_results[0].message


def test_execute_multiple_mixed_results(executor, setup_mock_tools):
    plan = PlanResult(steps=[
        PlanStep(tool="tool.success", args={"path": "ok"}),
        PlanStep(tool="tool.fail", args={"path": "bad"}),
    ])

    result = executor.execute(plan)
    assert len(result.step_results) == 2
    assert "Failed:" in result.step_results[1].message


def test_execute_unknown_tool(executor, setup_mock_tools):
    plan = PlanResult(steps=[
        PlanStep(tool="tool.unknown", args={"path": "none"}),
    ])
    result = executor.execute(plan)
    assert len(result.step_results) == 1
    assert "Unknown tool" in result.step_results[0].message


def test_execute_handles_exceptions(executor, setup_mock_tools):
    plan = PlanResult(steps=[
        PlanStep(tool="tool.exception", args={"path": "oops"}),
    ])
    result = executor.execute(plan)
    assert len(result.step_results) == 1
    assert "Error executing tool.exception" in result.step_results[0].message


def test_execute_empty_plan(executor):
    plan = PlanResult(steps=[])
    result = executor.execute(plan)
    assert len(result.step_results) == 1
    assert "No steps to execute" in result.step_results[0].message


def test_execution_summary_format(executor, setup_mock_tools):
    plan = PlanResult(steps=[
        PlanStep(tool="tool.success", args={"path": "ok"}),
        PlanStep(tool="tool.fail", args={"path": "bad"}),
    ])
    result = executor.execute(plan)
    summary = result.summary()

    assert "✅" in summary
    assert "❌" in summary
    assert "Listed:" in summary or "Failed:" in summary

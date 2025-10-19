import pytest
from src.core.planner import Planner
from src.models.plan import PlanStep, PlanResult


@pytest.fixture
def planner():
    return Planner()


# -----------------------------
# list_files tests
# -----------------------------
def test_generate_plan_list_files(planner):
    user_input = "list all files in ./docs"
    result = planner.generate_plan(user_input)

    assert isinstance(result, PlanResult)
    assert len(result.steps) == 1
    step = result.steps[0]
    assert step.tool == "list_files"
    assert step.args["path"] == "./docs"


def test_generate_plan_list_files_default(planner):
    user_input = "list files"
    result = planner.generate_plan(user_input)
    assert len(result.steps) == 1
    assert result.steps[0].args["path"] == "."


# -----------------------------
# read_file tests
# -----------------------------
def test_generate_plan_read_file(planner):
    user_input = "read file notes.txt"
    result = planner.generate_plan(user_input)
    assert len(result.steps) == 1
    step = result.steps[0]
    assert step.tool == "read_file"
    assert step.args["path"] == "notes.txt"


def test_generate_plan_read_file_missing_path(planner, capsys):
    user_input = "read file"
    result = planner.generate_plan(user_input)
    captured = capsys.readouterr()
    assert "Please specify the file path" in captured.out
    assert result.steps == []


# -----------------------------
# move_file tests
# -----------------------------
def test_generate_plan_move_file(planner):
    user_input = "move ./a.txt to ./b.txt"
    result = planner.generate_plan(user_input)
    assert len(result.steps) == 1
    step = result.steps[0]
    assert step.tool == "move_file"
    assert step.args["src"] == "./a.txt"
    assert step.args["dst"] == "./b.txt"


def test_generate_plan_move_file_invalid(planner):
    user_input = "move file"
    result = planner.generate_plan(user_input)
    # Should not add any steps if pattern not matched
    assert result.steps == []


# -----------------------------
# delete_file tests
# -----------------------------
def test_generate_plan_delete_file(planner):
    user_input = "delete file ./tmp.txt"
    result = planner.generate_plan(user_input)
    assert len(result.steps) == 1
    step = result.steps[0]
    assert step.tool == "delete_file"
    assert step.args["path"] == "./tmp.txt"
    assert step.args["confirm"] is False


def test_generate_plan_delete_file_missing_path(planner, capsys):
    user_input = "delete file"
    result = planner.generate_plan(user_input)
    captured = capsys.readouterr()
    assert "Please specify the file" in captured.out
    assert result.steps == []


# -----------------------------
# unknown command tests
# -----------------------------
def test_generate_plan_unknown_command(planner):
    user_input = "compress file logs.txt"
    result = planner.generate_plan(user_input)
    assert isinstance(result, PlanResult)
    assert result.steps == []

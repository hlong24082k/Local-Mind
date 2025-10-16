import os
import shutil
import pytest
from pathlib import Path
from src.tools import file_ops
from src.models.tool import ToolResult


# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    # Create some test files and folders
    f1 = tmp_path / "file1.txt"
    f2 = tmp_path / "file2.txt"
    f1.write_text("Hello World")
    f2.write_text("Test content")

    subdir = tmp_path / "subfolder"
    subdir.mkdir()
    return tmp_path


# -----------------------------
# Tests for list_files
# -----------------------------
def test_list_files_success(temp_dir):
    result = file_ops.list_files(temp_dir)
    assert isinstance(result, ToolResult)
    assert result.success is True
    assert "file1.txt" in result.message
    assert "file2.txt" in result.message


def test_list_files_invalid_path():
    result = file_ops.list_files("/invalid/path/xyz")
    assert result.success is False
    assert "Path not found" in result.message


# -----------------------------
# Tests for read_file
# -----------------------------
def test_read_file_success(temp_dir):
    file_path = temp_dir / "file1.txt"
    result = file_ops.read_file(str(file_path))
    assert result.success is True
    assert "Hello World" in result.message


def test_read_file_not_found():
    result = file_ops.read_file("/invalid/file.txt")
    assert result.success is False
    assert "Path not found" in result.message


# -----------------------------
# Tests for move_file
# -----------------------------
def test_move_file_success(temp_dir):
    src = temp_dir / "file1.txt"
    dst = temp_dir / "moved.txt"
    result = file_ops.move_file(str(src), str(dst))
    assert result.success is True
    assert "Moved" in result.message  # typo fix: should be "message" in function
    assert not src.exists()
    assert dst.exists()


def test_move_file_not_found(temp_dir):
    src = temp_dir / "missing.txt"
    dst = temp_dir / "moved.txt"
    result = file_ops.move_file(str(src), str(dst))
    assert result.success is False
    assert "Path not found" in result.message


# -----------------------------
# Tests for delete_file
# -----------------------------
def test_delete_file_success(temp_dir):
    f = temp_dir / "delete_me.txt"
    f.write_text("bye")
    result = file_ops.delete_file(str(f))
    assert result.success is True
    assert "Deleted" in result.message  # typo fix: should be "message"
    assert not f.exists()


def test_delete_file_not_found():
    result = file_ops.delete_file("/invalid/file.txt")
    assert result.success is False
    assert "Path not found" in result.message

import os
import shutil

from pathlib import Path
from src.models.tool import ToolResult


def list_files(path=".") -> ToolResult:
    path = os.path.expanduser(path)
    p = Path(path)
    if not p.exists():
        return ToolResult(
            success=False,
            message=f"Path not found: {path}",
        )
    files = [str(f) for f in p.iterdir() if f.is_file()]
    files_str = "\n".join(files)
    if files:
        return ToolResult(
            success=True,
            message=files_str,
        )
    else:
        return ToolResult(
            success=False,
            message=f"Path not found: {path}",
        )


def read_file(path) -> ToolResult:
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return ToolResult(
            success=False,
            message=f"Path not found: {path}",
        )
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read(500)  # Limit for CLI preview
    return ToolResult(
        success=True,
        message=f"--- Begin of {path} ---\n{content}\n--- End of preview ---",
    )


def move_file(src, dst) -> ToolResult:
    src, dst = os.path.expanduser(src), os.path.expanduser(dst)
    if not os.path.exists(src):
        return ToolResult(
            success=False,
            message=f"Path not found: {src}",
        )
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)
    return ToolResult(
        success=True,
        message=f"Moved {src} → {dst}"
    )


def delete_file(path, confirm=True) -> ToolResult:
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return ToolResult(
            success=False,
            message=f"Path not found: {path}",
        )
    os.remove(path)
    return ToolResult(
        success=True,
        message=f"Deleted {path}"
    )

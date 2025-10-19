from src.tools.tool_registry import ToolRegistry
from src.tools.file_ops import (
    list_files,
    read_file,
    move_file,
    delete_file
)

ToolRegistry.register('tool.list_files', list_files)
ToolRegistry.register('tool.read_file', read_file)
ToolRegistry.register('tool.move_file', move_file)
ToolRegistry.register('tool.delete_file', delete_file)

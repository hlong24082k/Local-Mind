from src.tools.tool_registry import ToolRegistry
from src.tools.file_ops import (
    list_files,
    read_file,
    move_file,
    delete_file
)

ToolRegistry.register('list_files', list_files)
ToolRegistry.register('read_file', read_file)
ToolRegistry.register('move_file', move_file)
ToolRegistry.register('delete_file', delete_file)

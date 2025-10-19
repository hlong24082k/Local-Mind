from pydantic import BaseModel
from typing import Optional, Callable, List


class ToolResult(BaseModel):
    success: bool
    message: str


class ToolDef(BaseModel):
    name: str
    description: Optional[str] = ""
    func: Callable
    required_args: List[str]

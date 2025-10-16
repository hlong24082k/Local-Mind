from pydantic import BaseModel


class ToolResult(BaseModel):
    success: bool
    message: str

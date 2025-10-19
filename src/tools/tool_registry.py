import inspect

from typing import Dict, Callable, List
from src.models.tool import ToolDef


class ToolRegistry:
    _tools: Dict[str, ToolDef] = {}

    @classmethod
    def register(cls, name: str, func: Callable):
        sig = inspect.signature(func)
        arg_names = list(sig.parameters.keys())

        cls._tools[name] = ToolDef(
            name=name,
            func=func,
            required_args=arg_names
        )

    @classmethod
    def get(cls, name: str):
        return cls._tools.get(name)

    @classmethod
    def names(cls) -> List[str]:
        return list(cls._tools.keys())

# src/models/validation.py
from pydantic import BaseModel
from typing import List


class ValidationResult(BaseModel):
    success: bool
    errors: List[str] = []
    warnings: List[str] = []

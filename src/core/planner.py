import re

from src.models.plan import PlanStep, PlanResult


class Planner:
    """
    Simple rule-based planner to simulate intent parsing before LLM integration.
    Returns a list of action dicts with 'tool' and 'args'.
    """
    def generate_plan(self, user_input: str) -> PlanResult:
        user_input = user_input.lower()
        plan = PlanResult(steps=[])
        # list files
        if "list" in user_input and "file" in user_input:
            parts = re.findall(f"(\.\/\w+|\.\/|\.)", user_input)
            path = parts[0] if parts else "."

            plan.add_step(PlanStep(tool="list_files", args={"path": path}))
            return plan

        # read file
        if "read" in user_input:
            path = self._extract_path(user_input)
            if not path:
                print("Please specify the file path (e.g., 'read file notes.txt').")
                return plan
            plan.add_step(PlanStep(tool="read_file", args={"path": path}))
            return plan

        # move file
        if "move" in user_input:
            parts = re.findall(r"move\s+(.+?)\s+to\s+(.+)", user_input)
            if parts:
                src, dst = parts[0]
                plan.add_step(PlanStep(tool="move_file", args={"src": src.strip(), "dst": dst.strip()}))
                return plan

        # delete file
        if "delete" in user_input or "remove" in user_input:
            path = self._extract_path(user_input)
            if not path:
                print("Please specify the file to delete.")
                return plan
            plan.add_step(PlanStep(tool="delete_file", args={"path": path, "confirm": False}))
            return plan
        return plan

    @staticmethod
    def _extract_path(text: str):
        # Very basic path detection, e.g., "read file ./test.txt"
        match = re.search(r"\b(\.\/\S+|\~\/\S+|\/\S+|\w+\.\w+)\b", text)
        return match.group(1) if match else None

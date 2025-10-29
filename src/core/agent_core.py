from loguru import logger

from src.core.executor import Executor
from src.core.planner import Planner
from src.core.validator import PlanValidator


class AgentCore:
    def __init__(self):
        self.planner = Planner()
        self.validator = PlanValidator()
        self.executor = Executor()

    def run(self, input_data: str):
        plan = self.planner.generate_plan(input_data)
        logger.debug(f"Generated Plan: {plan}")

        validation = self.validator.validate(plan)

        if not validation.success:
            logger.error(f"Plan validation failed: {validation.errors}")
            return validation

        execution = self.executor.execute(plan)
        logger.debug(f"Execution Result: {execution}")
        return execution
    

if __name__ == "__main__":
    agent = AgentCore()
    input_data = "list files in ./src/core"
    result = agent.run(input_data)
    print(result)  # Replace with appropriate result handling

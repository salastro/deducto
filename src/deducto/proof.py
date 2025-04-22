from typing import List, Optional
from deducto.expr import *
from deducto.rules.apply import *

class ProofStep:
    def __init__(self, result: Expr, rule: str, premises: List[int]):
        self.result = result
        self.rule = rule
        self.premises = premises

    def __str__(self):
        if self.premises:
            premises_str = ', '.join(str(i + 1) for i in self.premises)
            return f"{self.result}    ({self.rule} from {premises_str})"
        else:
            return f"{self.result}    ({self.rule})"

class ProofState:
    def __init__(self, assumptions: List[Expr], goal: Expr):
        self.assumptions = assumptions
        self.goal = goal
        self.steps: List[ProofStep] = [ProofStep(a, "assumption", []) for a in assumptions]

    def show(self):
        print("\nProof Steps:")
        for i, step in enumerate(self.steps):
            print(f"{i + 1}. {step}")
        print("\nGoal:")
        print(f"  {self.goal}")

    def try_rule(self, rule: str, premise_indices: List[int]) -> bool:
        try:
            premises = [self.steps[i].result for i in premise_indices]
            result = apply_rule(rule, premises)
            if result is None:
                print(f"✗ Rule '{rule}' not applicable to given premises.")
                return False
            self.steps.append(ProofStep(result, rule, premise_indices))
            if result == self.goal:
                print("✓ Goal reached!")
            return True
        except IndexError:
            print("✗ Invalid premise index.")
            return False

    # def list_applicable(self):
    #     formulas = [step.result for step in self.steps]
    #     suggestions = list_applicable_rules(formulas, self.goal)
    #     if suggestions:
    #         print("Possible rules to try:")
    #         for rule, premises in suggestions:
    #             indices = ', '.join(str(i + 1) for i in premises)
    #             print(f"  {rule} on steps {indices}")
    #     else:
    #         print("No obvious applicable rules found.")

from typing import List
from deducto.core.expr import *
from deducto.rules.apply import *
from deducto.cli.utils import parse_path, resolve_path, set_path

class ProofStep:
    def __init__(self, result: Expr, rule: str, premises: List[int]):
        self.result = result
        self.rule = rule
        self.premises = premises

    def __str__(self):
        if self.premises:
            premises_str = ', '.join(str(i + 1) for i in self.premises)
            rule = self.rule.replace("_", " ")
            return f"{self.result}		({rule} of {premises_str})"
        else:
            return f"{self.result}		({self.rule})"

class ProofState:
    def __init__(self, assumptions: List[Expr], goal: Expr):
        self.assumptions = assumptions
        self.goal = goal
        self.steps: List[ProofStep] = [ProofStep(a, "assumption", []) for a in assumptions]

    def show(self):
        print("\nProof Steps:")
        for i, step in enumerate(self.steps):
            print(f"  {i + 1}. {step}")
        print(f"Goal: {self.goal}")

    def try_rule(self, rule: str, targets: List[str]) -> bool:
        try:
            if '.' in targets[0]:  # handle subexpression
                idx, path = parse_path(targets[0])
                expr = deepcopy(self.steps[idx].result)
                subexpr = resolve_path(expr, path)
                result = apply_rule(rule, [subexpr])
                if result is None:
                    print(f"✗ Rule '{rule}' not applicable at {targets[0]}")
                    return False
                set_path(expr, path, result)
                subnode = '.'.join(targets[0].split('.')[1:])
                self.steps.append(ProofStep(expr, f"{rule} at {subnode}", [idx]))
            else:
                premise_indices = [int(t) - 1 for t in targets]
                premises = [self.steps[i].result for i in premise_indices]
                result = apply_rule(rule, premises)
                if result is None:
                    print(f"✗ Rule '{rule}' not applicable to given premises.")
                    return False
                self.steps.append(ProofStep(result, rule, premise_indices))

            if self.steps[-1].result == self.goal:
                print("✓ Goal reached!")
                self.show()
            return True

        except IndexError:
            print("✗ Invalid step index.")
            return False
        except Exception as e:
            print(f"✗ Error applying rule: {e}")
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

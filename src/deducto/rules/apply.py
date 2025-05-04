"""
Available rules:
addition, conjunction, disjunctive_syllogism, hypothetical_syllogism,
modus_ponens, modus_tollens, resolution, simplification, absorption_and,
absorption_or, associative_and, associative_or, biconditional_elimination,
commutative_and, commutative_or, demorgan_and, demorgan_or, distributive_and,
distributive_or, idempotent, identity_and, identity_or, material_implication,
negation, xor_decomposition.
"""
from deducto.core.expr import *
from deducto.rules import inference, equivalence
from typing import List
import inspect

def list_rules() -> List[str]:
    rules = []
    for module in [inference, equivalence]:
        for name in dir(module):
            obj = getattr(module, name)
            if inspect.isfunction(obj) and not name.startswith("_"):
                rules.append(name)
    return rules

def apply_rule(rule: str, premises: List[Expr]) -> Expr:
    """
    Apply a rule to the given premises.
    ---
    :param rule: The name of the rule to apply.
    :param premises: A list of premises (Expr objects).
    :return: The result of applying the rule, or None if not applicable.
    :raises ValueError: If the rule given does not exist (or at least is not implemented)
    """
    rules = list_rules()
    # Check if the rule exists in the inference or equivalence modules
    if rule in rules:
        # Get the function object for the rule
        rule_func = getattr(inference, rule, None) or getattr(equivalence, rule, None)
        if rule_func:
            # Call the function with the premises
            return rule_func(*premises)

    else:
        raise ValueError(f"Rule '{rule}' does not exist")

# def list_applicable_rules(premises: List[Expr], goal: Expr):
#     suggestions = []
#     for i, a in enumerate(premises):
#         for j, b in enumerate(premises):
#             if i != j and isinstance(b, Implies) and a == b.premise and b.conclusion == goal:
#                 suggestions.append(("modus_ponens", [i, j]))
#         if isinstance(a, And):
#             if a.left == goal:
#                 suggestions.append(("and_elim_left", [i]))
#             if a.right == goal:
#                 suggestions.append(("and_elim_right", [i]))
#         if isinstance(goal, And):
#             for j, b in enumerate(premises):
#                 if b == goal.left:
#                     for k, c in enumerate(premises):
#                         if c == goal.right:
#                             suggestions.append(("and_intro", [j, k]))
#         if isinstance(a, Iff):
#             if goal == Implies(a.left, a.right):
#                 suggestions.append(("iff_elim_left", [i]))
#             if goal == Implies(a.right, a.left):
#                 suggestions.append(("iff_elim_right", [i]))
#     return suggestions

def get_rule_explanation(rule: str) -> str:
    """
    Get the explanation (docstring) of the rule given
    ---
    :param rule: The name of the rule
    :return: The docstring of the rule
    :raises ValueError: If the rule given does not exist (or at least is not implemented)
    """
    rules = list_rules()
    # Check if the rule exists in the inference or equivalence modules
    if rule in rules:
        # Get the function object for the rule
        rule_func = getattr(inference, rule, None) or getattr(equivalence, rule, None)
        explanation = rule_func.__doc__
        if explanation:
            # Remove leading/trailing whitespace and newlines
            explanation = explanation.strip()
            return explanation
        else:
            return f"No explanation available for rule '{rule}'"
    else:
        raise ValueError(f"Rule '{rule}' does not exist")

if __name__ == '__main__':
    from deducto.parser import parse
    from copy import deepcopy

    def resolve_path(expr, path):
        """Access a nested attribute path like ['left', 'right']"""
        for attr in path:
            expr = getattr(expr, attr)
        return expr

    def set_path(expr, path, new_value):
        """Mutate a subexpression via a path"""
        for attr in path[:-1]:
            expr = getattr(expr, attr)
        setattr(expr, path[-1], new_value)

    def parse_path(path_str):
        """Convert '1.left.right' to (premise_index, ['left', 'right'])"""
        parts = path_str.split('.')
        return int(parts[0]) - 1, parts[1:]

    # Input variables
    variables = input("Enter variables (comma-separated): ").strip()
    variables = [v.strip() for v in variables.split(",")]
    print(f"Variables: {variables}")

    # Input premises
    premises = input("Enter premises (comma-separated): ").strip()
    if not premises:
        premises = []
        print("No premises provided.")
    else:
        premises = [parse(p.strip()) for p in premises.split(",")]
        print("Premises:")
        for i, p in enumerate(premises):
            print(f"  {i + 1}. {p}")

    # Input goal
    goal = input("Enter goal: ").strip()
    goal = parse(goal) if goal else None
    if goal:
        print(f"Goal: {goal}")
    else:
        print("No goal provided.")

    # REPL loop
    while True:
        cmd = input("Enter rule to apply (or 'exit' to quit): ").strip()
        if cmd.lower() == 'exit':
            break
        try:
            parts = cmd.split()
            rule = parts[0]
            targets = parts[1:]

            results = []
            for ref in targets:
                if '.' in ref:
                    idx, path = parse_path(ref)
                    expr = deepcopy(premises[idx])  # to avoid mutating the original
                    subexpr = resolve_path(expr, path)
                    result = apply_rule(rule, [subexpr])
                    if result is None:
                        raise ValueError(f"Rule '{rule}' not applicable at {ref}")
                    set_path(expr, path, result)
                    results.append(expr)
                else:
                    idx = int(ref) - 1
                    results.append(premises[idx])

            # If only one argument and it was a path, treat it as the whole new result
            result = results[0] if len(results) == 1 and '.' in targets[0] else apply_rule(rule, results)

            if result is None:
                print(f"Rule '{rule}' not applicable.")
            else:
                print(f"Result: {result}")
                if result == goal:
                    break
                premises.append(result)
                print("Premises:")
                for i, p in enumerate(premises):
                    print(f"  {i + 1}. {p}")

        except Exception as e:
            print(f"Invalid: {e}")

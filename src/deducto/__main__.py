from deducto.expr import *
from deducto.rules.inference import *
from deducto.rules.equivalence import *
from deducto.rules.apply import *
from deducto.parser import parse
from deducto.utils import *

if __name__ == '__main__':
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
                    print("✓ Goal reached!")
                    break
                premises.append(result)
                print("Premises:")
                for i, p in enumerate(premises):
                    print(f"  {i + 1}. {p}")

        except Exception as e:
            print(f"Invalid: {e}")

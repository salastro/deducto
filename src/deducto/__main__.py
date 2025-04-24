from deducto.expr import *
from deducto.rules.inference import *
from deducto.rules.equivalence import *
from deducto.rules.apply import *
from deducto.parser import parse
from deducto.repl import *
from copy import deepcopy
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

def all_paths(expr, prefix=""):
    paths = []

    # Unary operator: has only 'operand' (e.g., NOT operation)
    if hasattr(expr, 'operand'):
        path = f"{prefix}operand" if not prefix else f"{prefix}.operand"
        paths.append(path)
        paths.extend(all_paths(expr.operand, path))

    # Binary operator: has 'left' and 'right'
    elif hasattr(expr, 'left') and hasattr(expr, 'right'):
        for attr in ["left", "right"]:
            subexpr = getattr(expr, attr)
            path = f"{prefix}{attr}" if not prefix else f"{prefix}.{attr}"
            paths.append(path)
            paths.extend(all_paths(subexpr, path))

    return paths

if __name__ == '__main__':
    # Prompt toolkit setup
    rule_completer = WordCompleter(list_rules(), ignore_case=True)
    rule_session = PromptSession(completer=rule_completer)

    # Input variables
    variables = PromptSession().prompt("Variables: ").strip()
    print("\033[F\033[K", end="") # Clear the line
    variables = [v.strip() for v in variables.split(",")]
    print(f"Variables: {variables}")

    operators = ["->", "<->", "&", "|", "!", "^", "T", "F"]
    input_completer = WordCompleter(variables+operators, ignore_case=True)
    input_session = PromptSession(completer=input_completer)

    # Input premises
    premises = input_session.prompt("Premises: ").strip()
    print("\033[F\033[K", end="") # Clear the line
    if not premises:
        premises = []
        print("No premises provided.")
    else:
        premises = [parse(p.strip()) for p in premises.split(",")]
        print("Premises:")
        for i, p in enumerate(premises):
            print(f"  {i + 1}. {p}")

    # Input goal
    goal = input_session.prompt("Goal: ").strip()
    print("\033[F\033[K", end="") # Clear the line
    goal = parse(goal) if goal else None
    if goal:
        print(f"Goal: {goal}")
    else:
        print("No goal provided.")

    # Update completer dynamically for premises references
    def update_rule_completer():
        rule_names = list_rules()
        premise_refs = [str(i+1) for i in range(len(premises))]
        rule_completer.words = rule_names + premise_refs + [f"{i+1}.{path}" for i, p in enumerate(premises) for path in all_paths(p)]

    # REPL loop
    while True:
        try:
            update_rule_completer()
            cmd = rule_session.prompt("Enter rule to apply (or 'exit' to quit): ").strip()
            if cmd.lower() == 'exit':
                break

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

            result = results[0] if len(results) == 1 and '.' in targets[0] else apply_rule(rule, results)

            if result is None:
                print(f"Rule '{rule}' not applicable.")
            else:
                print(f"Result: {result}")
                if result == goal:
                    print("\u2713 Goal reached!")
                    break
                premises.append(result)
                print("Premises:")
                for i, p in enumerate(premises):
                    print(f"  {i + 1}. {p}")

        except EOFError:
            confirm = input("\nExit? (y/n): ")
            if confirm.lower() == 'y':
                print(2*"\033[F\033[K", end="") # Clear the line
                break
            print(3*"\033[F\033[K", end="") # Clear the line

        except Exception as e:
            print(f"Invalid: {e}")

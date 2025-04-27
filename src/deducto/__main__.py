from deducto.expr import *
from deducto.rules.inference import *
from deducto.rules.equivalence import *
from deducto.rules.apply import *
from deducto.parser import parse
from deducto.repl import *
from copy import deepcopy
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from deducto.proof import ProofState, ProofStep


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

def main():
    # Prompt toolkit setup
    rule_completer = WordCompleter(list_rules(), ignore_case=True)
    rule_session = PromptSession(completer=rule_completer)

    # Input variables
    variables = PromptSession().prompt("Variables: ").strip()
    print("\033[F\033[K", end="") # Clear the line
    variables = [v.strip() for v in variables.split(",")]
    print(f"Variables: {variables}")

    operators = ["->", "<->", "&", "|", "!", "^", "T", "F"]
    input_completer = WordCompleter(variables + operators, ignore_case=True)
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

    # ProofState
    proof = ProofState(premises, goal)
    initial_steps = deepcopy(proof.steps)  # For reset

    # Update completer dynamically
    def update_rule_completer():
        rule_names = list_rules()
        step_refs = [str(i+1) for i in range(len(proof.steps))]
        subpaths = [f"{i+1}.{path}" for i, step in enumerate(proof.steps) for path in all_paths(step.result)]
        rule_completer.words = rule_names + step_refs + subpaths + ['undo', 'delete', 'reset', 'exit']

    print("Commands: [rule targets], undo, delete n, reset, exit")

    while True:
        try:
            update_rule_completer()
            cmd = rule_session.prompt("Apply: ").strip()
            if cmd.lower() == 'exit':
                break

            if cmd.lower() == 'undo':
                if len(proof.steps) > len(initial_steps):
                    proof.steps.pop()
                    print("Undone last operation.")
                else:
                    print("Nothing to undo.")
                proof.show()
                continue

            if cmd.lower().startswith('delete '):
                try:
                    n = int(cmd.split()[1]) - 1
                    if n >= len(initial_steps):
                        proof.steps.pop(n)
                        print(f"Deleted step {n + 1}.")
                    else:
                        print("Cannot delete original assumptions.")
                except Exception as e:
                    print(f"Invalid delete command: {e}")
                proof.show()
                continue

            if cmd.lower() == 'reset':
                proof.steps = deepcopy(initial_steps)
                print("Reset to original assumptions.")
                proof.show()
                continue

            parts = cmd.split()
            rule = parts[0]
            targets = parts[1:]

            if not targets:
                print("No targets specified.")
                continue

            if '.' in targets[0]:  # If targeting subexpression
                idx, path = parse_path(targets[0])
                expr = deepcopy(proof.steps[idx].result)
                subexpr = resolve_path(expr, path)
                result = apply_rule(rule, [subexpr])
                if result is None:
                    raise ValueError(f"Rule '{rule}' not applicable at {targets[0]}")
                set_path(expr, path, result)
                proof.steps.append(ProofStep(expr, f"{rule} at {idx+1}.{path}", [idx]))
                if expr == proof.goal:
                    print("✓ Goal reached!")
                    proof.show()
                    break
            else:
                premise_indices = [int(t) - 1 for t in targets]
                success = proof.try_rule(rule, premise_indices)
                if success and proof.steps[-1].result == proof.goal:
                    proof.show()
                    break

            proof.show()

        except EOFError:
            confirm = input("\nExit? (y/n): ")
            if confirm.lower() == 'y':
                print(2*"\033[F\033[K", end="") # Clear the line
                break
            print(3*"\033[F\033[K", end="") # Clear the line

        except Exception as e:
            print(f"Invalid: {e}")
    

if __name__ == '__main__':
    main()

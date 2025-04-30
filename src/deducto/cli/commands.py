from copy import deepcopy
from deducto.rules.apply import apply_rule, list_rules
from deducto.core.proof import ProofStep
from deducto.cli.utils import all_paths, parse_path, resolve_path, set_path

def update_rule_completer(completer, proof):
    rule_names = list_rules()
    step_refs = [str(i+1) for i in range(len(proof.steps))]
    subpaths = [f"{i+1}.{path}" for i, step in enumerate(proof.steps) for path in all_paths(step.result)]
    completer.words = rule_names + step_refs + subpaths + ['undo', 'delete', 'reset', 'exit']

def execute_command(cmd, proof, initial_steps):
    if cmd.lower() == 'exit':
        return True

    if cmd.lower() == 'undo':
        if len(proof.steps) > len(initial_steps):
            proof.steps.pop()
            print("Undone last operation.")
        else:
            print("Nothing to undo.")
        return False

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
        return False

    if cmd.lower() == 'reset':
        proof.steps = deepcopy(initial_steps)
        print("Reset to original assumptions.")
        return False

    parts = cmd.split()
    rule = parts[0]
    targets = parts[1:]

    if not targets:
        print("No targets specified.")
        return False

    if '.' in targets[0]:  # subexpression
        idx, path = parse_path(targets[0])
        expr = deepcopy(proof.steps[idx].result)
        subexpr = resolve_path(expr, path)
        result = apply_rule(rule, [subexpr])
        if result is None:
            raise ValueError(f"Rule '{rule}' not applicable at {targets[0]}")
        set_path(expr, path, result)
        proof.steps.append(ProofStep(expr, f"{rule} at {path}", [idx]))
    else:
        indices = [int(t) - 1 for t in targets]
        proof.try_rule(rule, indices)

    if proof.goal and proof.steps[-1].result == proof.goal:
        # print("✓ Goal reached!")
        return True

    return False

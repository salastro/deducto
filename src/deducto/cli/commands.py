from copy import deepcopy

from prompt_toolkit.completion import Completer, WordCompleter, NestedCompleter
from prompt_toolkit.document import Document

from deducto.cli.utils import all_paths, parse_path, resolve_path, set_path
from deducto.core.proof import ProofStep
from deducto.rules.apply import apply_rule, list_rules

class CommandCompleter(Completer):
    def __init__(self, proof):
        self.proof = proof
        self.rules = list_rules()
        self.commands = ['apply', 'undo', 'delete', 'reset', 'exit']

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lstrip()
        stripped_len = len(document.text_before_cursor) - len(text)

        if " " in text:
            command = text.split()[0]
            if command in self.commands:
                remaining_text = text[len(command):].lstrip()
                move_cursor = len(text) - len(remaining_text) + stripped_len

                new_document = Document(
                    remaining_text,
                    cursor_position=document.cursor_position - move_cursor,
                )

                if command == 'apply':
                    parts = remaining_text.split()
                    if not parts:
                        # Suggest rules only
                        completer = WordCompleter(self.rules, ignore_case=True)
                    else:
                        rule = parts[0]
                        if rule in self.rules:
                            # After rule is entered, suggest step refs and subpaths
                            step_refs = [str(i + 1) for i in range(len(self.proof.steps))]
                            subpaths = [
                                f"{i + 1}.{path}"
                                for i, step in enumerate(self.proof.steps)
                                for path in all_paths(step.result)
                            ]
                            completer = WordCompleter(step_refs + subpaths, ignore_case=True)
                        else:
                            # Suggest rules if the entered rule is incomplete or invalid
                            completer = WordCompleter(self.rules, ignore_case=True)

                    yield from completer.get_completions(new_document, complete_event)

                elif command == 'undo':
                    pass  # Placeholder for future undo completions

                elif command in ['reset', 'exit']:
                    pass  # These take no arguments, no completions needed

        else:
            # Complete command names
            completer = WordCompleter(self.commands, ignore_case=True)
            yield from completer.get_completions(document, complete_event)

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

    if cmd.lower().startswith('apply '):

        parts = cmd.split()
        rule = parts[1]
        targets = parts[2:]

        if not targets:
            print("No targets specified.")
            return False

        if '.' in targets[0]:  # subexpression
            node = targets[0][2:]
            idx, path = parse_path(targets[0])
            expr = deepcopy(proof.steps[idx].result)
            subexpr = resolve_path(expr, path)
            result = apply_rule(rule, [subexpr])
            if result is None:
                raise ValueError(f"Rule '{rule}' not applicable at {targets[0]}")
            set_path(expr, path, result)
            proof.steps.append(ProofStep(expr, f"{rule} at {node}", [idx]))
        else:
            indices = [int(t) - 1 for t in targets]
            proof.try_rule(rule, indices)

    if proof.goal and proof.steps[-1].result == proof.goal:
        return True

    return False

from copy import deepcopy

from prompt_toolkit.completion import Completer, WordCompleter, NestedCompleter
from prompt_toolkit.document import Document

from deducto.core.utils import all_paths, parse_path, resolve_path, set_path
from deducto.core.proof import ProofStep
from deducto.rules.apply import list_rules, get_rule_explanation
from deducto.export.tex import export_tex
from deducto.export.txt import export_txt
from deducto.cli.parser import parse


class CommandCompleter(Completer):
    def __init__(self, proof):
        self.proof = proof
        self.rules = list_rules()
        self.commands = ['apply', 'undo', 'delete', 'reset', 'exit', 'export', 'assume', 'goal', 'help', 'list']

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

                elif command == 'delete':
                    # Suggest step refs for delete and undo commands
                    step_refs = [str(i + 1) for i in range(len(self.proof.steps))]
                    completer = WordCompleter(step_refs, ignore_case=True)
                    yield from completer.get_completions(new_document, complete_event)

                elif command == 'help':
                    parts = remaining_text.split()
                    if (
                        len(parts) == 0 or (len(parts) == 1 and remaining_text[-1] != " ")
                    ): # the rule is not or not fully entered
                        completer = WordCompleter(self.rules, ignore_case=True)
                        yield from completer.get_completions(new_document, complete_event)

        else:
            # Complete command names
            completer = WordCompleter(self.commands, ignore_case=True)
            yield from completer.get_completions(document, complete_event)


def undo_last_step(proof, initial_steps):
    if len(proof.steps) > len(initial_steps):
        proof.steps.pop()
        print("Undone last operation.")
    else:
        print("Nothing to undo.")

def delete_step(proof, n):
    if n < len(proof.steps):
        proof.steps.pop(n)
        print(f"Deleted step {n + 1}.")
    else:
        print("Cannot delete original assumptions.")

def reset_proof(proof, initial_steps):
    proof.steps = deepcopy(initial_steps)
    print("Reset to original assumptions.")


def execute_command(cmd, proof, initial_steps):
    parts = cmd.split()
    if cmd.lower() == 'exit':
        return True

    if cmd.lower() == 'list':
        print("Available rules:")
        for rule in list_rules():
            print(f"  {rule}")
        return False

    if cmd.lower().startswith('help'):
        if len(parts) == 1:
            print("Commands:")
            print("  apply <rule> <target> - Apply a rule to the specified targets.")
            print("  goal <goal> - Set the goal expression.")
            print("  assume <premise> - Add an assumption.")
            print("  list - List available rules.")
            print("  exact - Check if the goal is reached.")
            print("  undo - Undo the last step.")
            print("  delete <n> - Delete step n.")
            print("  reset - Reset to original assumptions.")
            print("  export <format> <filename> - Export proof to specified format.")
            print("  exit - Exit the session.")
            print("  help - Show this help message.")
            print("  help <rule> - Get help about a rule.")
        elif len(parts) == 2:
            rule = parts[1]
            print(get_rule_explanation(rule))
        else:
            print("Usage: help or help <rule>")
        return False

    if cmd.lower() == 'undo':
        undo_last_step(proof, initial_steps)
        return False

    if cmd.lower().startswith('delete '):
        try:
            n = int(cmd.split()[1]) - 1
            delete_step(proof, n)
        except Exception as e:
            print(f"Invalid delete command: {e}")
        return False

    if cmd.lower() == 'reset':
        reset_proof(proof, initial_steps)
        return False

    if cmd.lower().startswith('export '):
        if len(parts) != 3:
            print("Usage: export <format> <filename>")
            return False
        fmt = parts[1]
        filename = parts[2]
        if fmt == "tex":
            export_tex(proof, filename)
            print(f"✓ Exported to {filename}.tex and {filename}.pdf")
        elif fmt == "txt":
            export_txt(proof, filename)
        else:
            print("Unknown format. Supported formats: tex, txt")
        return False

    if cmd.lower().startswith('goal '):
        if len(parts) < 2:
            print("Usage: goal <goal>")
            return False
        goal_str = ' '.join(parts[1:])
        try:
            proof.goal = parse(goal_str)
            print(f"✓ Goal updated to: {proof.goal}")
        except Exception as e:
            print(f"✗ Failed to parse goal: {e}")
        return False

    if cmd.lower().startswith('assume '):
        if len(parts) < 2:
            print("Usage: assume <premise>")
            return False
        assumption_str = ' '.join(parts[1:])
        if not assumption_str:
            print("✗ No assumption provided.")
            return False
        try:
            expr = parse(assumption_str)
            proof.assumptions.append(expr)
            proof.steps.append(ProofStep(expr, "assumption", []))
            print(f"✓ Assumption added: {expr}")
        except Exception as e:
            print(f"✗ Failed to parse assumption: {e}")
        return False

    if cmd.lower() == 'exact':
        if proof.goal is None:
            print("No goal set.")
            return False
        if proof.steps[-1].result == proof.goal:
            print("✓ Goal reached!")
            return True
        else:
            print("✗ Goal not reached.")
            return False

    if cmd.lower().startswith('apply '):
        rule = parts[1]
        targets = parts[2:]

        if not targets:
            print("No targets specified.")
            return False

        proof.try_rule(rule, targets)

    else:
        raise ValueError(f"Unknown command '{cmd}'")

    if proof.goal and proof.steps[-1].result == proof.goal:
        return True

    return False

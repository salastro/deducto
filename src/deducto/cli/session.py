from copy import deepcopy

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from deducto.cli.commands import execute_command, CommandCompleter
from deducto.cli.utils import get_goal, get_premises, get_variables
from deducto.core.proof import ProofState
from deducto.export.tex import generate_structured_latex_from_proofstate


def clear_line():
    """Clears one line in the output"""
    print("\033[F\033[K", end="")

def run_proof_session():
    variables = get_variables()
    clear_line()
    print("Variables:", ", ".join(variables))
    while True:
        try:
            premises = get_premises(variables)
            break
        except SyntaxError as e:
            print(f"Invalid syntax: {e}")
    clear_line()
    if premises:
        print("Premises:")
        for i, premise in enumerate(premises):
            print(f"  {i + 1}. {premise}")
    else:
        print("No premises provided")
    while True:
        try:
            goal = get_goal(variables)
            break
        except SyntaxError as e:
            print(f"Invalid syntax: {e}")
    clear_line()
    if goal:
        print("Goal:", goal)
    else:
        print("No goal provided")

    proof = ProofState(premises, goal)
    initial_steps = deepcopy(proof.steps)

    completer = CommandCompleter(proof)
    session = PromptSession(completer=completer)

    print("Commands: apply <rule> <targets>, undo, delete <n>, reset, exit")

    while True:
        try:
            cmd = ""
            while cmd == "":
                cmd = session.prompt(">>> ").strip()
            if execute_command(cmd, proof, initial_steps):
                export = input("Export to LaTeX? (y/n): ").lower()
                if export == 'y':
                    filepath = input("Enter output path prefix (no extension): ").strip()
                    generate_structured_latex_from_proofstate(proof, filepath)
                    print(f"✓ Exported to {filepath}.tex and {filepath}.pdf")
                else:
                    print("Export skipped.")
                break
            proof.show()
        except (KeyboardInterrupt, EOFError):
            if input("\nExit? (y/n): ").lower() == 'y':
                break
        except Exception as e:
            print(f"Invalid: {e}")

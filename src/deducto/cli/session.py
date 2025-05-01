from copy import deepcopy

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from deducto.cli.commands import execute_command, CommandCompleter
from deducto.cli.utils import get_goal, get_premises, get_variables
from deducto.core.proof import ProofState
from deducto.export.tex import generate_structured_latex_from_proofstate


def run_proof_session():

    variables = get_variables()
    print("\033[F\033[K", end="")
    print("Variables:", variables)
    premises = get_premises(variables)
    print("\033[F\033[K", end="")
    print("Premises:")
    for i, premise in enumerate(premises):
        print(f"  {i + 1}. {premise}")
    goal = get_goal(variables)
    print("\033[F\033[K", end="")
    print("Goal:", goal)

    proof = ProofState(premises, goal)
    initial_steps = deepcopy(proof.steps)

    completer = CommandCompleter(proof)
    session = PromptSession(completer=completer)

    print("Commands: apply <rule> <targets>, undo, delete <n>, reset, exit")

    while True:
        try:
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
        except EOFError:
            if input("\nExit? (y/n): ").lower() == 'y':
                break
        except Exception as e:
            print(f"Invalid: {e}")

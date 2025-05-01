from copy import deepcopy

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from deducto.cli.commands import execute_command, CommandCompleter
from deducto.cli.utils import get_goal, get_premises, get_variables
from deducto.core.proof import ProofState


def clear_line():
    """Clears one line in the output"""
    print("\033[F\033[K", end="")

def run_proof_session():
    variables = get_variables()
    clear_line()
    print("Variables:", variables)
    premises = get_premises(variables)
    clear_line()
    print("Premises:")
    for i, premise in enumerate(premises):
        print(f"  {i + 1}. {premise}")
    goal = get_goal(variables)
    clear_line()
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
                break
            proof.show()
        except EOFError:
            if input("\nExit? (y/n): ").lower() == 'y':
                break
        except Exception as e:
            print(f"Invalid: {e}")

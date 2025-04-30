from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from copy import deepcopy

from deducto.cli.parser import parse
from deducto.core.proof import ProofState, ProofStep
from deducto.cli.utils import get_variables, get_premises, get_goal
from deducto.cli.commands import execute_command, update_rule_completer

def run_proof_session():
    rule_completer = WordCompleter([], ignore_case=True)
    rule_session = PromptSession(completer=rule_completer)

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

    print("Commands: [rule targets], undo, delete n, reset, exit")

    while True:
        try:
            update_rule_completer(rule_completer, proof)
            cmd = rule_session.prompt(">>> ").strip()
            if execute_command(cmd, proof, initial_steps):
                break
            proof.show()
        except EOFError:
            if input("\nExit? (y/n): ").lower() == 'y':
                break
        except Exception as e:
            print(f"Invalid: {e}")


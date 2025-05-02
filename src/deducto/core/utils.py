from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from deducto.cli.parser import parse


def get_variables():
    session = PromptSession()
    variables = session.prompt("Variables: ").strip()
    # print("\033[F\033[K", end="")
    return [v.strip() for v in variables.split(",")]

def get_premises(variables):
    operators = ["->", "<->", "&", "|", "!", "^", "T", "F"]
    input_session = PromptSession(completer=WordCompleter(variables + operators, ignore_case=True))
    raw = input_session.prompt("Premises: ").strip()
    # print("\033[F\033[K", end="")
    return [parse(p.strip()) for p in raw.split(",")] if raw else []

def get_goal(variables):
    operators = ["->", "<->", "&", "|", "!", "^", "T", "F"]
    input_session = PromptSession(completer=WordCompleter(variables + operators, ignore_case=True))
    goal = input_session.prompt("Goal: ").strip()
    # print("\033[F\033[K", end="")
    return parse(goal) if goal else None

def resolve_path(expr, path):
    """Access a nested attribute path like ['left', 'right']"""
    for attr in path:
        expr = getattr(expr, attr)
    return expr

def set_path(expr, path, new_value):
    """Mutate a subexpression via a path"""
    for attr in path[:-1]:
        expr = getattr(expr, attr)
    setattr(expr, path[-1], new_value)

def parse_path(path_str):
    """Convert '1.left.right' to (premise_index, ['left', 'right'])"""
    parts = path_str.split('.')
    return int(parts[0]) - 1, parts[1:]

def all_paths(expr, prefix=""):
    paths = []
    if hasattr(expr, 'negated'):
        path = f"{prefix}negated" if not prefix else f"{prefix}.negated"
        paths.append(path)
        paths.extend(all_paths(expr.negated, path))
    elif hasattr(expr, 'left') and hasattr(expr, 'right'):
        for attr in ["left", "right"]:
            subexpr = getattr(expr, attr)
            path = f"{prefix}{attr}" if not prefix else f"{prefix}.{attr}"
            paths.append(path)
            paths.extend(all_paths(subexpr, path))
    return paths

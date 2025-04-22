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


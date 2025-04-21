from deducto.expr import *

def commutative_and(expr: And) -> And:
    """
    Commutative property of And
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    return And(expr.right, expr.left)


def associative_and(expr: And) -> And:
    """
    Associative property of And
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    if not isinstance(expr.left, And):
        raise TypeError("Expected the left operand to be an instance of And")
    return And(expr.left.left, And(expr.left.right, expr.right))
    

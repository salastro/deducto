from deducto.core.expr import *

def commutative_and(expr: And) -> And:
    """
    And(a, b) = And(b, a)
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    return And(expr.right, expr.left)


def associative_and(expr: And) -> And:
    """
    And(And(a, b), c) = And(a, And(b, c))
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    if not isinstance(expr.left, And):
        raise TypeError("Expected the left operand to be an instance of And")
    return And(expr.left.left, And(expr.left.right, expr.right))
    
def commutative_or(expr: Or) -> Or:
    """
    Or(a, b) = Or(b, a)
    """
    if not isinstance(expr, Or):
        raise TypeError("Expected an instance of Or")
    return Or(expr.right, expr.left)

def associative_or(expr: Or) -> Or:
    """
    Or(Or(a, b), c) = Or(a, Or(b, c))
    """
    if not isinstance(expr, Or):
        raise TypeError("Expected an instance of Or")
    if not isinstance(expr.left, Or):
        raise TypeError("Expected the left operand to be an instance of Or")
    return Or(expr.left.left, Or(expr.left.right, expr.right))

def distributive_and(expr: And) -> Or:
    """
    Distributive property of And over Or
    And(a, Or(b, c)) = Or(And(a, b), And(a, c))
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    if not isinstance(expr.right, Or):
        raise TypeError("Expected the left operand to be an instance of Or")
    return Or(And(expr.left, expr.right.left), And(expr.left, expr.right.right))

def distributive_or(expr: Or) -> And:
    """
    Distributive property of Or over And
    Or(a, And(b, c)) = And(Or(a, b), Or(a, c))
    """
    if not isinstance(expr, Or):
        raise TypeError("Expected an instance of Or")
    if not isinstance(expr.right, And):
        raise TypeError("Expected the left operand to be an instance of And")
    return And(Or(expr.left, expr.right.left), Or(expr.left, expr.right.right))

def idempotent(expr: Expr) -> Expr:
    """
    Idempotent property of And and Or
    And(a, a) = a
    Or(a, a) = a
    """
    if not isinstance(expr, And) and not isinstance(expr, Or):
        raise TypeError("Expected an instance of And or Or")
    if expr.left != expr.right:
        raise ValueError("Operands are not equal")
    return expr.left

def absorption_and(expr: And) -> Expr:
    """
    Absorption property
    And(a, Or(a, b)) = a
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    if not isinstance(expr.right, Or):
        raise TypeError("Expected the right operand to be an instance of Or")
    if expr.left != expr.right.left:
        raise ValueError("Operands are not equal")
    return expr.left

def absorption_or(expr: Or) -> Expr:
    """
    Absorption property
    Or(a, And(a, b)) = a
    """
    if not isinstance(expr, Or):
        raise TypeError("Expected an instance of Or")
    if not isinstance(expr.right, And):
        raise TypeError("Expected the right operand to be an instance of And")
    if expr.left != expr.right.left:
        raise ValueError("Operands are not equal")
    return expr.left

def demorgan_and(expr: Not) -> Or:
    """
    De Morgan's law for And
    Not(And(a, b)) = Or(Not(a), Not(b))
    """
    if not isinstance(expr, Not):
        raise TypeError("Expected an instance of And")
    negated = expr.negated
    if not isinstance(negated, And):
        raise TypeError("Expected the operand to be an instance of And")
    return Or(Not(negated.left), Not(negated.right))

def demorgan_or(expr: Not) -> And:
    """
    De Morgan's law for Or
    Not(Or(a, b)) = And(Not(a), Not(b))
    """
    if not isinstance(expr, Not):
        raise TypeError("Expected an instance of Or")
    negated = expr.negated
    if not isinstance(negated, Or):
        raise TypeError("Expected the operand to be an instance of Or")
    return And(Not(negated.left), Not(negated.right))

def negation(expr: Not) -> Expr:
    """
    Negation property
    Not(Not(a)) = a
    """
    if not isinstance(expr, Not):
        raise TypeError("Expected an instance of Not")
    return expr.negated.negated

def identity_or(expr: Or) -> Expr:
    """
    Identity Law of Or
    Or(a, False) = a
    """
    if not isinstance(expr, Or):
        raise TypeError("Expected an instance of Or")
    if expr.right != FalseExpr:
        raise ValueError("Right operand is not False")
    return expr.left

def identity_and(expr: And) -> Expr:
    """
    Identity Law of And
    And(a, True) = a
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    if expr.right != TrueExpr():
        raise ValueError("Right operand is not True")
    return expr.left

def domination_or(expr: Or) -> TrueExpr:
    """
    Domination Law of Or
    Or(a, True) = True
    """
    if not isinstance(expr, Or):
        raise TypeError("Expected an instance of Or")
    if expr.right != TrueExpr():
        raise ValueError("Right operand is not True")
    return TrueExpr()

def domination_and(expr: And) -> FalseExpr:
    """
    Domination Law of And
    And(a, False) = False
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    if expr.right != FalseExpr():
        raise ValueError("Right operand is not False")
    return FalseExpr()

def contradiction(expr: And) -> FalseExpr:
    """
    And(a, Not(a)) = False
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    if expr.right != Not(expr.left):
        raise ValueError("Right operand is not False")
    return FalseExpr()

def excluded_middle(expr: Or) -> TrueExpr:
    """
    Or(a, Not(a)) = True
    """
    if not isinstance(expr, Or):
        raise TypeError("Expected an instance of Or")
    if expr.right != Not(expr.left):
        raise ValueError("Right operand is not the negation of the left operand")
    return TrueExpr()

def material_implication(expr: Implies) -> Or:
    """
    Implies(P, Q) = Or(Not(P), Q)
    """
    if not isinstance(expr, Implies):
        raise TypeError("Expected an instance of Implies")
    return Or(Not(expr.left), expr.right)

def biconditional_elimination(expr: Iff) -> And:
    """
    Iff(P, Q) = And(Implies(P, Q), Implies(Q, P))
    """
    if not isinstance(expr, Iff):
        raise TypeError("Expected an instance of Iff")
    return And(Implies(expr.left, expr.right), Implies(expr.right, expr.left))

def xor_decomposition(expr: Xor) -> Or:
    """
    Xor(P, Q) = And(Or(P, Q), Not(And(P, Q)))
    """
    if not isinstance(expr, Xor):
        raise TypeError("Expected an instance of Xor")
    return And(Or(expr.left, expr.right), Not(And(expr.left, expr.right)))

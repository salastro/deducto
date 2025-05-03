from deducto.core.expr import *


def commutative_and(expr: And) -> And:
    """
    a ∧ b ⇔ b ∧ a
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    return And(expr.right, expr.left)

def associative_and(expr: And) -> And:
    """
    (a ∧ b) ∧ c ⇔ a ∧ (b ∧ c)
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    if not isinstance(expr.left, And):
        raise TypeError("Expected the left operand to be an instance of And")
    return And(expr.left.left, And(expr.left.right, expr.right))

def commutative_or(expr: Or) -> Or:
    """
    a ∨ b ⇔ b ∨ a
    """
    if not isinstance(expr, Or):
        raise TypeError("Expected an instance of Or")
    return Or(expr.right, expr.left)

def associative_or(expr: Or) -> Or:
    """
    (a ∨ b) ∨ c ⇔ a ∨ (b ∨ c)
    """
    if not isinstance(expr, Or):
        raise TypeError("Expected an instance of Or")
    if not isinstance(expr.left, Or):
        raise TypeError("Expected the left operand to be an instance of Or")
    return Or(expr.left.left, Or(expr.left.right, expr.right))

def distributive_and(expr: And) -> Or:
    """
    a ∧ (b ∨ c) ⇔ (a ∧ b) ∨ (a ∧ c)
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    if not isinstance(expr.right, Or):
        raise TypeError("Expected the left operand to be an instance of Or")
    return Or(And(expr.left, expr.right.left), And(expr.left, expr.right.right))

def distributive_or(expr: Or) -> And:
    """
    a ∨ (b ∧ c) ⇔ (a ∨ b) ∧ (a ∨ c)
    """
    if not isinstance(expr, Or):
        raise TypeError("Expected an instance of Or")
    if not isinstance(expr.right, And):
        raise TypeError("Expected the left operand to be an instance of And")
    return And(Or(expr.left, expr.right.left), Or(expr.left, expr.right.right))

def idempotent(expr: Expr) -> Expr:
    """
    a ∧ a ⇔ a
    a ∨ a ⇔ a
    """
    if not isinstance(expr, And) and not isinstance(expr, Or):
        raise TypeError("Expected an instance of And or Or")
    if expr.left != expr.right:
        raise ValueError("Operands are not equal")
    return expr.left

def absorption_and(expr: And) -> Expr:
    """
    a ∧ (a ∨ b) ⇔ a
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
    a ∨ (a ∧ b) ⇔ a
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
    ¬(a ∧ b) ⇔ ¬a ∨ ¬b
    """
    if not isinstance(expr, Not):
        raise TypeError("Expected an instance of And")
    negated = expr.negated
    if not isinstance(negated, And):
        raise TypeError("Expected the operand to be an instance of And")
    return Or(Not(negated.left), Not(negated.right))

def demorgan_or(expr: Not) -> And:
    """
    ¬(a ∨ b) ⇔ ¬a ∧ ¬b
    """
    if not isinstance(expr, Not):
        raise TypeError("Expected an instance of Or")
    negated = expr.negated
    if not isinstance(negated, Or):
        raise TypeError("Expected the operand to be an instance of Or")
    return And(Not(negated.left), Not(negated.right))

def negation(expr: Not) -> Expr:
    """
    ¬(¬a) ⇔ a
    """
    if not isinstance(expr, Not):
        raise TypeError("Expected an instance of Not")
    if not isinstance(expr.negated, Not):
        raise TypeError("Expected double negation")
    return expr.negated.negated

def identity_or(expr: Or) -> Expr:
    """
    a ∨ F ⇔ a
    """
    if not isinstance(expr, Or):
        raise TypeError("Expected an instance of Or")
    if expr.right != FalseExpr:
        raise ValueError("Right operand is not False")
    return expr.left

def identity_and(expr: And) -> Expr:
    """
    a ∧ T ⇔ a
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    if expr.right != TrueExpr():
        raise ValueError("Right operand is not True")
    return expr.left

def domination_or(expr: Or) -> TrueExpr:
    """
    a ∨ T ⇔ T
    """
    if not isinstance(expr, Or):
        raise TypeError("Expected an instance of Or")
    if expr.right != TrueExpr():
        raise ValueError("Right operand is not True")
    return TrueExpr()

def domination_and(expr: And) -> FalseExpr:
    """
    a ∧ F ⇔ F
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    if expr.right != FalseExpr():
        raise ValueError("Right operand is not False")
    return FalseExpr()

def contradiction(expr: And) -> FalseExpr:
    """
    a ∧ ¬a ⇔ F
    """
    if not isinstance(expr, And):
        raise TypeError("Expected an instance of And")
    if expr.right != Not(expr.left):
        raise ValueError("Right operand is not False")
    return FalseExpr()

def excluded_middle(expr: Or) -> TrueExpr:
    """
    a ∨ ¬a ⇔ T
    """
    if not isinstance(expr, Or):
        raise TypeError("Expected an instance of Or")
    if expr.right != Not(expr.left):
        raise ValueError("Right operand is not the negation of the left operand")
    return TrueExpr()

def material_implication(expr: Implies) -> Or:
    """
    P → Q ⇔ ¬P ∨ Q
    """
    if not isinstance(expr, Implies):
        raise TypeError("Expected an instance of Implies")
    return Or(Not(expr.left), expr.right)

def biconditional_elimination(expr: Iff) -> And:
    """
    P ↔ Q ⇔ (P → Q) ∧ (Q → P)
    """
    if not isinstance(expr, Iff):
        raise TypeError("Expected an instance of Iff")
    return And(Implies(expr.left, expr.right), Implies(expr.right, expr.left))

def xor_decomposition(expr: Xor) -> Or:
    """
    P ⊕ Q ⇔ (P ∨ Q) ∧ ¬(P ∧ Q)
    """
    if not isinstance(expr, Xor):
        raise TypeError("Expected an instance of Xor")
    return And(Or(expr.left, expr.right), Not(And(expr.left, expr.right)))

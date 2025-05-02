from deducto.core.expr import *

def modus_ponens(implication: Implies, premise: Expr):
    """
    premise: P
    implication: P → Q
    conclusion: Q
    """
    if not isinstance(implication, Implies):
        raise TypeError("Invalid type for modus ponens: Expected Implies for implication")
    if implication.left == premise:
        return implication.right
    raise TypeError("Premise does not match the left side of the implication")

def modus_tollens(implication: Implies, negation: Not):
    """
    negation: ¬Q
    implication: P → Q
    conclusion: ¬P
    """
    if not isinstance(implication, Implies):
        raise TypeError("Invalid type for modus tollens: Expected Implies for implication")
    if not isinstance(negation, Not):
        raise TypeError("Invalid type for modus tollens: Expected Not for negation")
    if Not(implication.right) == negation:
        return Not(implication.left)
    raise TypeError("Negation does not match the right side of the implication")

def hypothetical_syllogism(implication1: Implies, implication2: Implies):
    """
    implication1: P → Q
    implication2: Q → R
    conclusion: P → R
    """
    if not isinstance(implication1, Implies):
        raise TypeError("Invalid type for hypothetical syllogism: Expected Implies for implication1")
    if not isinstance(implication2, Implies):
        raise TypeError("Invalid type for hypothetical syllogism: Expected Implies for implication2")
    if implication1.right == implication2.left:
        return Implies(implication1.left, implication2.right)
    raise TypeError("The right side of implication1 does not match the left side of implication2")

def disjunctive_syllogism(disjunction: Or, negation: Not):
    """
    disjunction: P ∨ Q
    negation: ¬P
    conclusion: Q
    """
    if not isinstance(disjunction, Or):
        raise TypeError("Invalid type for disjunctive syllogism: Expected Or for disjunction")
    if not isinstance(negation, Not):
        raise TypeError("Invalid type for disjunctive syllogism: Expected Not for negation")
    if Not(disjunction.left) == negation:
        return disjunction.right
    raise TypeError("Negation does not match the left side of the disjunction")

def addition(premise: Expr, antecedent: Expr):
    """
    premise: P
    conclusion: P ∨ Q
    """
    return Or(premise, antecedent)

def simplification(conjunction: And):
    """
    conjunction: P ∧ Q
    conclusion: P
    """
    if not isinstance(conjunction, And):
        raise TypeError("Invalid type for simplification: Expected And for conjunction")
    return conjunction.left

def conjunction(antecedent: Expr, consequent: Expr):
    """
    antecedent: P
    consequent: Q
    conclusion: P ∧ Q
    """
    return And(antecedent, consequent)

def resolution(disjunction1: Or, disjunction2: Or):
    """
    disjunction1: P ∨ Q
    disjunction2: ¬P ∨ R
    """
    if not isinstance(disjunction1, Or):
        raise TypeError("Invalid type for resolution: Expected Or for disjunction1")
    if not isinstance(disjunction2, Or):
        raise TypeError("Invalid type for resolution: Expected Or for disjunction2")
    if Not(disjunction1.left) == disjunction2.left:
        return Or(disjunction1.right, disjunction2.right)
    raise TypeError("The left side of disjunction1 does not match the negated left side of disjunction2")

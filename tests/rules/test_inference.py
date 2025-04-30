import pytest
from deducto.core.expr import *
from deducto.rules.inference import *

# Test for modus_ponens
def test_modus_ponens():
    p = Var("P")
    q = Var("Q")
    implication = Implies(p, q)
    
    # Valid case
    result = modus_ponens(implication, p)
    assert result == q

    # Invalid case: premise does not match the left side
    with pytest.raises(TypeError):
        modus_ponens(implication, Var("R"))

# Test for modus_tollens
def test_modus_tollens():
    p = Var("P")
    q = Var("Q")
    implication = Implies(p, q)
    negation = Not(q)

    # Valid case
    result = modus_tollens(implication, negation)
    assert result == Not(p)

    # Invalid case: negation does not match the right side
    with pytest.raises(TypeError):
        modus_tollens(implication, Not(Var("R")))

# Test for hypothetical_syllogism
def test_hypothetical_syllogism():
    p = Var("P")
    q = Var("Q")
    r = Var("R")
    implication1 = Implies(p, q)
    implication2 = Implies(q, r)

    # Valid case
    result = hypothetical_syllogism(implication1, implication2)
    assert result == Implies(p, r)

    # Invalid case: implications don't connect properly
    with pytest.raises(TypeError):
        hypothetical_syllogism(implication1, Implies(r, q))

# Test for disjunctive_syllogism
def test_disjunctive_syllogism():
    p = Var("P")
    q = Var("Q")
    disjunction = Or(p, q)
    negation = Not(p)

    # Valid case
    result = disjunctive_syllogism(disjunction, negation)
    assert result == q

    # Invalid case: negation does not match the left side
    with pytest.raises(TypeError):
        disjunctive_syllogism(disjunction, Not(Var("R")))

# Test for addition
def test_addition():
    p = Var("P")
    q = Var("Q")
    
    # Valid case
    result = addition(p, q)
    assert result == Or(p, q)

# Test for simplification
def test_simplification():
    p = Var("P")
    q = Var("Q")
    conjunction = And(p, q)

    # Valid case
    result = simplification(conjunction)
    assert result == p

    # Invalid case: not an And
    with pytest.raises(TypeError):
        simplification(Var("R"))

# Test for conjunction
def test_conjunction():
    p = Var("P")
    q = Var("Q")

    # Valid case
    result = conjunction(p, q)
    assert result == And(p, q)


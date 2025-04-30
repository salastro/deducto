import pytest
from deducto.core.expr import *
from deducto.rules.equivalence import *

def test_commutative_and():
    p = Var("P")
    q = Var("Q")
    pq = And(p, q)
    qp = And(q, p)

    # Valid case
    result = commutative_and(pq)
    assert result == qp

    # Invalid case: expected an instance of And
    with pytest.raises(TypeError):
        commutative_and(Or(p, q))

def test_associative_and():
    p = Var("P")
    q = Var("Q")
    r = Var("R")
    pqr1 = And(And(p, q), r)
    pqr2 = And(p, And(q, r))

    result = associative_and(pqr1)
    assert result == pqr2

    with pytest.raises(TypeError):
        associative_and(And(p, And(q, r)))

    with pytest.raises(TypeError):
        associative_and(Or(p, And(q, r)))

    with pytest.raises(TypeError):
        associative_and(And(Or(p, q), r))

def test_commutative_or():
    p = Var("P")
    q = Var("Q")
    pq = Or(p, q)
    qp = Or(q, p)

    # Valid case
    result = commutative_or(pq)
    assert result == qp

    # Invalid case: expected an instance of Or
    with pytest.raises(TypeError):
        commutative_or(And(p, q))

def test_associative_or():
    p = Var("P")
    q = Var("Q")
    r = Var("R")
    pqr1 = Or(Or(p, q), r)
    pqr2 = Or(p, Or(q, r))

    result = associative_or(pqr1)
    assert result == pqr2

    with pytest.raises(TypeError):
        associative_or(Or(p, Or(q, r)))

    with pytest.raises(TypeError):
        associative_or(And(p, Or(q, r)))

def test_distributive_and():
    p = Var("P")
    q = Var("Q")
    r = Var("R")
    and_expr = And(p, Or(q, r))
    expected = Or(And(p, q), And(p, r))

    result = distributive_and(and_expr)
    assert result == expected

    with pytest.raises(TypeError):
        distributive_and(Or(p, q))

    with pytest.raises(TypeError):
        distributive_and(And(p, And(q, r)))

def test_distributive_or():
    p = Var("P")
    q = Var("Q")
    r = Var("R")
    or_expr = Or(p, And(q, r))
    expected = And(Or(p, q), Or(p, r))

    result = distributive_or(or_expr)
    assert result == expected

    with pytest.raises(TypeError):
        distributive_or(And(p, q))

    with pytest.raises(TypeError):
        distributive_or(Or(And(q, r), p))

def test_idempotent():
    p = Var("P")
    expr1 = And(p, p)
    expr2 = Or(p, p)

    result_and = idempotent(expr1)
    assert result_and == p

    result_or = idempotent(expr2)
    assert result_or == p

    with pytest.raises(ValueError):
        idempotent(And(p, Var("Q")))

def test_absorption_and():
    p = Var("P")
    q = Var("Q")
    r = Var("R")
    and_expr = And(p, Or(p, q))

    result = absorption_and(and_expr)
    assert result == p

    with pytest.raises(ValueError):
        absorption_and(And(p, Or(q, r)))

    with pytest.raises(TypeError):
        absorption_and(Or(p, And(q, r)))

def test_absorption_or():
    p = Var("P")
    q = Var("Q")
    r = Var("R")
    or_expr = Or(p, And(p, q))

    result = absorption_or(or_expr)
    assert result == p

    with pytest.raises(ValueError):
        absorption_or(Or(p, And(q, r)))

    with pytest.raises(TypeError):
        absorption_or(And(p, Or(q, r)))

def test_demorgan_and():
    p = Var("P")
    q = Var("Q")
    and_expr = Not(And(p, q))

    result = demorgan_and(and_expr)
    expected = Or(Not(p), Not(q))
    assert result == expected

    with pytest.raises(TypeError):
        demorgan_and(Or(p, q))

def test_demorgan_or():
    p = Var("P")
    q = Var("Q")
    or_expr = Not(Or(p, q))

    result = demorgan_or(or_expr)
    expected = And(Not(p), Not(q))
    assert result == expected

    with pytest.raises(TypeError):
        demorgan_or(And(p, q))

def test_negation():
    p = Var("P")
    q = Var("Q")
    not_expr = Not(Not(p))

    result = negation(not_expr)
    assert result == p

    with pytest.raises(TypeError):
        negation(And(p, q))

def test_identity_or():
    p = Var("P")
    or_expr = Or(p, FalseExpr)

    result = identity_or(or_expr)
    assert result == p

    with pytest.raises(ValueError):
        identity_or(Or(p, TrueExpr))

def test_identity_and():
    p = Var("P")
    and_expr = And(p, TrueExpr())

    result = identity_and(and_expr)
    assert result == p

    with pytest.raises(ValueError):
        identity_and(And(p, FalseExpr))

def test_domination_or():
    p = Var("P")
    or_expr = Or(p, TrueExpr())

    result = domination_or(or_expr)
    assert isinstance(result, TrueExpr)

def test_domination_and():
    F = FalseExpr()
    p = Var("P")
    and_expr = And(p, F)

    result = domination_and(and_expr)
    assert result == F

def test_contradiction():
    F = FalseExpr()
    p = Var("P")
    and_expr = And(p, Not(p))

    result = contradiction(and_expr)
    assert result == F

def test_excluded_middle():
    T = TrueExpr()
    p = Var("P")
    or_expr = Or(p, Not(p))

    result = excluded_middle(or_expr)
    assert result == T

def test_material_implication():
    p = Var("P")
    q = Var("Q")
    implies_expr = Implies(p, q)

    result = material_implication(implies_expr)
    expected = Or(Not(p), q)
    assert result == expected

def test_biconditional_elimination():
    p = Var("P")
    q = Var("Q")
    iff_expr = Iff(p, q)

    result = biconditional_elimination(iff_expr)
    expected = And(Implies(p, q), Implies(q, p))
    assert result == expected

def test_xor_decomposition():
    p = Var("P")
    q = Var("Q")
    xor_expr = Xor(p, q)

    result = xor_decomposition(xor_expr)
    expected = And(Or(p, q), Not(And(p, q)))
    assert result == expected

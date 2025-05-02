import pytest
from deducto.cli.parser import parse
from deducto.core.expr import *

def test_single_var():
    assert parse("P") == Var("P")

def test_not():
    assert parse("¬P") == Not(Var("P"))
    assert parse("!P") == Not(Var("P"))
    assert parse("NOT P") == Not(Var("P"))

def test_and():
    assert parse("P ∧ Q") == And(Var("P"), Var("Q"))
    assert parse("P AND Q") == And(Var("P"), Var("Q"))
    assert parse("P & Q") == And(Var("P"), Var("Q"))

def test_or():
    assert parse("P ∨ Q") == Or(Var("P"), Var("Q"))
    assert parse("P OR Q") == Or(Var("P"), Var("Q"))
    assert parse("P | Q") == Or(Var("P"), Var("Q"))

def test_implies():
    assert parse("P → Q") == Implies(Var("P"), Var("Q"))
    assert parse("P -> Q") == Implies(Var("P"), Var("Q"))
    assert parse("P IMPLIES Q") == Implies(Var("P"), Var("Q"))

def test_iff():
    assert parse("P ↔ Q") == Iff(Var("P"), Var("Q"))
    assert parse("P <-> Q") == Iff(Var("P"), Var("Q"))
    assert parse("P IFF Q") == Iff(Var("P"), Var("Q"))

def test_xor():
    assert parse("P ⊕ Q") == Xor(Var("P"), Var("Q"))
    assert parse("P ^ Q") == Xor(Var("P"), Var("Q"))
    assert parse("P XOR Q") == Xor(Var("P"), Var("Q"))

def test_constants():
    assert parse("T") == TrueExpr()
    assert parse("F") == FalseExpr()
    assert parse("TRUE") == TrueExpr()
    assert parse("FALSE") == FalseExpr()

def test_parentheses():
    expr = parse("(P ∨ Q) ∧ R")
    assert expr == And(Or(Var("P"), Var("Q")), Var("R"))

def test_precedence():
    # ¬ binds tightest, then ∧, then ∨, then →, then ↔
    expr = parse("¬P ∨ Q ∧ R → S")
    # Parsed as: ((Not(P)) ∨ (Q ∧ R)) → S
    assert expr == Implies(Or(Not(Var("P")), And(Var("Q"), Var("R"))), Var("S"))

def test_nested():
    expr = parse("((P))")
    assert expr == Var("P")

def test_multiple_iff():
    expr = parse("P ↔ Q ↔ R")
    # Should group left-to-right: Iff(Iff(P, Q), R)
    assert expr == Iff(Iff(Var("P"), Var("Q")), Var("R"))

def test_invalid_token():
    with pytest.raises(SyntaxError):
        parse("P @ Q")

def test_unmatched_paren():
    with pytest.raises(SyntaxError):
        parse("(P ∨ Q")

def test_unexpected_end():
    with pytest.raises(SyntaxError):
        parse("P ∧")

def test_missing_operand():
    with pytest.raises(SyntaxError):
        parse("¬")


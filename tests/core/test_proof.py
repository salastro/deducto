import pytest
from deducto.core.proof import ProofStep, ProofState
from deducto.core.expr import Var, Not, And, Or
from deducto.core.utils import parse_path, resolve_path, set_path

def test_proofstep_str_with_premises():
    step = ProofStep(Var("A"), "modus_ponens", [0, 1])
    assert str(step) == "A		(modus ponens of 1, 2)"

def test_proofstep_str_without_premises():
    step = ProofStep(Var("A"), "assumption", [])
    assert str(step) == "A		(assumption)"

def test_proofstate_initialization():
    A = Var("A")
    B = Var("B")
    goal = And(A, B)
    proof = ProofState([A, B], goal)
    assert len(proof.steps) == 2
    assert proof.steps[0].result == A
    assert proof.steps[1].result == B
    assert proof.goal == goal

def test_try_rule_simple_and_intro():
    A = Var("A")
    B = Var("B")
    goal = And(A, B)
    proof = ProofState([A, B], goal)
    success = proof.try_rule("conjunction", ["1", "2"])
    assert success
    assert proof.steps[-1].result == goal
    assert "conjunction" in proof.steps[-1].rule

def test_try_rule_invalid_step_index():
    A = Var("A")
    B = Var("B")
    proof = ProofState([A], B)
    success = proof.try_rule("conjunction", ["1", "3"])  # Invalid index
    assert not success

def test_try_rule_invalid_rule_name():
    A = Var("A")
    proof = ProofState([A], Not(A))
    success = proof.try_rule("nonexistent_rule", ["1"])
    assert not success

def test_try_rule_with_path_mutation():
    expr = Or(Not(Not(Var("A"))), Var("B"))
    goal = Or(Var("A"), Var("B"))
    proof = ProofState([expr], goal)
    success = proof.try_rule("negation", ["1.left"])
    assert success
    assert proof.steps[-1].result == goal
    assert "negation" in proof.steps[-1].rule

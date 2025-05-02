# tests/test_cli_utils.py

import pytest
from deducto.cli import utils
from deducto.core.expr import *

def test_resolve_path():
    expr = And(Var("A"), Var("B"))
    path = ["left"]
    assert utils.resolve_path(expr, path) == Var("A")

def test_set_path():
    expr = And(Var("A"), Var("B"))
    utils.set_path(expr, ["right"], Var("C"))
    assert expr.right == Var("C")

def test_parse_path():
    index, path = utils.parse_path("2.left.right")
    assert index == 1
    assert path == ["left", "right"]

def test_all_paths_simple_and():
    expr = And(Var("X"), Var("Y"))
    paths = utils.all_paths(expr)
    assert set(paths) == {"left", "right"}

def test_all_paths_nested():
    expr = Not(And(Var("P"), Or(Var("Q"), Var("R"))))
    paths = set(utils.all_paths(expr))
    expected = {
        "negated",
        "negated.left",
        "negated.right",
        "negated.right.left",
        "negated.right.right",
    }
    assert expected.issubset(paths)

def test_all_paths_deeply_nested():
    expr = Or(Not(Var("A")), And(Var("B"), Not(Var("C"))))
    paths = set(utils.all_paths(expr))
    assert "left.negated" in paths
    assert "right.left" in paths
    assert "right.right.negated" in paths


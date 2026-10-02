import ast
from textwrap import dedent

import pytest

from src.comparator import (
    ast_to_str,
    compare_ast,
    levenshtein_similarity,
    sequence_matcher_similarity,
    tree_edit_distance_similarity,
)


def parse_function(source: str) -> ast.FunctionDef | ast.AsyncFunctionDef:
    function = ast.parse(dedent(source)).body[0]
    assert isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef))
    return function


def test_ast_to_str_serializes_node_type_and_values() -> None:
    function = parse_function(
        """
        def add(value):
            return value + 1
        """
    )

    result = ast_to_str(function)

    assert result.startswith("FunctionDef add arguments arg value")
    assert "Return BinOp Name value Load Add Constant 1" in result


def test_sequence_matcher_similarity_is_one_for_equal_functions() -> None:
    function = parse_function(
        """
        def add(value):
            return value + 1
        """
    )

    assert sequence_matcher_similarity(function, function) == 1.0


def test_sequence_matcher_similarity_detects_different_functions() -> None:
    first = parse_function(
        """
        def add(value):
            return value + 1
        """
    )
    second = parse_function(
        """
        def multiply(value):
            return value * 2
        """
    )

    similarity = sequence_matcher_similarity(first, second)

    assert 0 <= similarity < 1


def test_levenshtein_similarity_is_one_for_equal_functions() -> None:
    pytest.importorskip("rapidfuzz")
    function = parse_function(
        """
        def add(value):
            return value + 1
        """
    )

    assert levenshtein_similarity(function, function) == 1.0


def test_tree_edit_distance_similarity_is_one_for_equal_functions() -> None:
    pytest.importorskip("apted")
    function = parse_function(
        """
        def add(value):
            return value + 1
        """
    )

    assert tree_edit_distance_similarity(function, function) == 1.0


@pytest.mark.parametrize("method", ["SQ", "LD", "TED"])
def test_compare_ast_dispatches_to_selected_method(method: str) -> None:
    if method == "LD":
        pytest.importorskip("rapidfuzz")
    elif method == "TED":
        pytest.importorskip("apted")

    function = parse_function(
        """
        def add(value):
            return value + 1
        """
    )

    assert compare_ast(function, function, method) == 100.0


def test_compare_ast_supports_async_functions() -> None:
    function = parse_function(
        """
        async def load():
            return 1
        """
    )

    assert compare_ast(function, function, "SQ") == 100.0


def test_compare_ast_rejects_unknown_method() -> None:
    function = parse_function(
        """
        def add(value):    
            return value + 1
        """
    )

    with pytest.raises(ValueError, match="UNKNOWN"):
        compare_ast(function, function, "UNKNOWN")

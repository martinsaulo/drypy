import ast
from difflib import SequenceMatcher


def ast_to_str(node: ast.AST) -> str:
    return ast.dump(node, annotate_fields=False, include_attributes=False)


def compare_ast(
        ast1: ast.FunctionDef | ast.AsyncFunctionDef, 
        ast2: ast.FunctionDef | ast.AsyncFunctionDef,
        method: str
    ) -> float:

    match method:
        case "SQ":
            compare = sequence_matcher_similarity
        case "LD":
            compare = levenshtein_similarity
        case "TED":
            compare = tree_edit_distance_similarity
        case _:
            raise ValueError(method)
            
    return compare(ast1, ast2) * 100


def sequence_matcher_similarity(
        ast1: ast.FunctionDef | ast.AsyncFunctionDef, 
        ast2: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> float:

    s1 = ast_to_str(ast1)
    s2 = ast_to_str(ast2)
    return SequenceMatcher(a=s1, b=s2).ratio()


def levenshtein_similarity(
        ast1: ast.FunctionDef | ast.AsyncFunctionDef, 
        ast2: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> float:

    try:
        from rapidfuzz.distance import Levenshtein
    except ImportError:
        ImportError("Para utilizar el método Levenshtein Distance (LD) es requerido instalar el paquete rapidfuzz.")

    s1 = ast_to_str(ast1)
    s2 = ast_to_str(ast2)

    distance = Levenshtein.distance(s1, s2)
    max_len = max(len(s1), len(s2))

    if max_len == 0:
        return 1.0

    return 1.0 - (distance / max_len)


def tree_edit_distance_similarity(
        ast1: ast.FunctionDef | ast.AsyncFunctionDef, 
        ast2: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> float:

    try:
        from apted import APTED
        from apted.helpers import Tree
    except ImportError:
        raise ImportError("Para utilizar el método Tree Edit Distance (TED) es requerido instalar el paquete apted.")

    def ast_to_apted_tree(node: ast.AST) -> Tree:
        label = type(node).__name__
        children = [ast_to_apted_tree(child) for child in ast.iter_child_nodes(node)]
        return Tree(label, *children)


    def apted_tree_size(tree: Tree) -> int:
        return 1 + sum(apted_tree_size(child) for child in tree.children)

    t1 = ast_to_apted_tree(ast1)
    t2 = ast_to_apted_tree(ast2)
    distance = APTED(t1, t2).compute_edit_distance()
    max_size = max(apted_tree_size(t1), apted_tree_size(t2))

    if max_size == 0:
        return 1.0

    return 1.0 - (distance / max_size)


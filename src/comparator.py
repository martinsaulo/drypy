import ast
from difflib import SequenceMatcher


def ast_to_str(node: ast.AST) -> str:
    return ast.dump(node, annotate_fields=False, include_attributes=False)


def compare_ast(
        ast1: ast.FunctionDef | ast.AsyncFunctionDef, 
        ast2: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> float:
    s1 = ast_to_str(ast1)
    s2 = ast_to_str(ast2)
    return SequenceMatcher(a=s1, b=s2).ratio() * 100
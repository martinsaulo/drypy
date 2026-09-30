import ast


def compare_ast(
        ast1: ast.FunctionDef | ast.AsyncFunctionDef, 
        ast2: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> float:
    return 1
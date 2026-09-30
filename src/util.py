# REMOVE
import ast
import json
from src.colors import BLUE, CYAN, END

SEPARATOR = f"{CYAN}-------------------------------------{END}"


def function_to_json(func: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    return json.dumps(ast_to_dict(func), indent=2, ensure_ascii=False)


def ast_to_dict(node):
    if isinstance(node, ast.AST):
        return {
            "type": type(node).__name__,
            **{
                field: ast_to_dict(value)
                for field, value in ast.iter_fields(node)
            }
        }

    if isinstance(node, list):
        return [ast_to_dict(item) for item in node]

    return node


def print_ast(func: ast.FunctionDef | ast.AsyncFunctionDef):
    print(SEPARATOR)
    print(f"{BLUE}Abstract Syntax Tree:{END}")
    print(function_to_json(func))


def print_code_from_ast(func: ast.FunctionDef | ast.AsyncFunctionDef):
    print(SEPARATOR)
    print(f"{BLUE}Generated Code:{END}")
    print(ast.unparse(func))
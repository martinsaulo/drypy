import ast
import copy
import os
from src.normalizer import normalize
from src.colors import CYAN, END


class FunctionDefinition:
    def __init__(
            self, 
            function: ast.FunctionDef | ast.AsyncFunctionDef, 
            file: str, 
            dir_path: str
        ):
        self.original_name = function.name
        self.node = function
        self.sub_tree = normalize(copy.deepcopy(function))
        self.file = file
        self.dir_path = os.path.normcase(os.path.abspath(dir_path))
        self.short_path = dir_path


    def __str__(self):
        return f"{self.short_path}{self.file}{CYAN}:{self.node.name}({self.file}:{self.node.lineno}){END}"


    def __eq__(self, value):
        return (
            self.dir_path == value.dir_path
            and self.file == value.file
            and self.original_name == value.original_name
        )



def extract_functions(file: str, dir_path: str) -> list[FunctionDefinition]:
    with open(os.path.join(dir_path, file), encoding="utf-8") as bytes_stream:
        node = ast.parse(bytes_stream.read())

    functions = [n for n in node.body if isinstance(n, ast.FunctionDef) or isinstance(n, ast.AsyncFunctionDef)]

    return [FunctionDefinition(n, file, dir_path) for n in functions]



def extract_target(target: str) -> FunctionDefinition:
    path, function = target.split(":")
    with open(path, encoding="utf-8") as bytes_stream:
        node = ast.parse(bytes_stream.read())

    n = next(filter(lambda x: x.name == function, node.body))
    dir_path, file = os.path.split(path)
    return FunctionDefinition(n, file, dir_path)



def extract_source(target: FunctionDefinition, max_lines: int = None) -> str:
    with open(os.path.join(target.dir_path, target.file), encoding="utf-8") as bytes_stream:
        source = bytes_stream.read()

    extracted = ast.get_source_segment(source, target.node)

    if extracted is None:
        return ""

    return "\n".join(extracted.splitlines()[:max_lines])
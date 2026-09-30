import ast
import copy
from src.normalizer import normalize
from src.colors import CYAN, END


class FunctionDefinition:
    def __init__(self, function, file, dir_path):
        self.original_name = function.name
        self.node = function
        self.sub_tree = normalize(copy.deepcopy(function))
        self.file = file
        self.dir_path = dir_path


    def __str__(self):
        return f"{self.dir_path}{self.file}{CYAN}:{self.node.name}({self.file}:{self.node.lineno}){END}"


    def __eq__(self, value):
        return self.dir_path == value.dir_path and self.file == self.file and self.original_name == value.original_name



def extract_functions(file, dir_path):
    with open(dir_path + file, encoding="utf-8") as bytes_stream:
        node = ast.parse(bytes_stream.read())

    functions = [n for n in node.body if isinstance(n, ast.FunctionDef) or isinstance(n, ast.AsyncFunctionDef)]

    return [FunctionDefinition(n, file, dir_path) for n in functions]



def extract_target(target):
    path, function = target.split(":")
    with open(path, encoding="utf-8") as bytes_stream:
        node = ast.parse(bytes_stream.read())

    n = next(filter(lambda x: x.name == function, node.body))
    file = path.split("/")[-1]
    dir_path = path.removesuffix(file)
    return FunctionDefinition(n, file, dir_path)



def extract_source(target, max_lines = None):
    with open(target.dir_path + target.file, encoding="utf-8") as bytes_stream:
        source = bytes_stream.read()

    extracted = ast.get_source_segment(source, target.node)

    if extracted is None:
        return ""

    return "\n".join(extracted.splitlines()[:max_lines])
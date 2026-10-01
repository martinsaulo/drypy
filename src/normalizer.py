import ast
import builtins
from enum import Enum


BUILTIN_NAMES = frozenset(dir(builtins))

def should_preserve_name(name: str) -> bool:
    return name in BUILTIN_NAMES


LITERALS = {
    int:       "INT",
    float:     "FLOAT",
    complex:   "COMPLEX",
    str:       "STR",
    bool:      "BOOL",
    bytes:     "BYTES",
    Ellipsis:  "ELLIPSIS",
}

class Symbol(Enum):
    VARIABLE   = "VAR"
    ARGUMENT   = "ARG"
    FUNCTION   = "FUNCTION_NAME"
    UNKNOWN    = "UNKN"


class Normalizer(ast.NodeTransformer):
    def __init__(self, function_name: str):
        super().__init__()
        
        self.function_name = function_name

        self.name_bindings = {
            Symbol.VARIABLE: {},
            Symbol.ARGUMENT: {},
        }

        self.symbols_count = {
            Symbol.VARIABLE: 0,
            Symbol.ARGUMENT: 0,
        }


    def get_or_add(self, name: str, symbol_type: Symbol) -> str:
        if name in self.name_bindings[symbol_type]:
            return self.name_bindings[symbol_type][name]

        new_binding = symbol_type.value + str(self.symbols_count[symbol_type])
        self.name_bindings[symbol_type][name] = new_binding
        self.symbols_count[symbol_type] += 1

        return new_binding


    def visit_Constant(self, node):
        if node.value != None:            
            node.value = LITERALS.get(type(node.value), Symbol.UNKNOWN.value)
        return node


    def visit_Name(self, node):
        if node.id == self.function_name:
            node.id = Symbol.FUNCTION.value
            return node

        if node.id in self.name_bindings[Symbol.ARGUMENT]:
            node.id = self.name_bindings[Symbol.ARGUMENT][node.id]
            return node

        if not should_preserve_name(node.id):
            node.id = self.get_or_add(node.id, Symbol.VARIABLE)

        return node


    def visit_arg(self, node):
        node.arg = self.get_or_add(node.arg, Symbol.ARGUMENT)
        return node


    def visit_Attribute(self, node):
        node.value = self.visit(node.value)
        return node



def normalize(
        tree: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> ast.FunctionDef | ast.AsyncFunctionDef:
    Normalizer(tree.name).visit(tree)
    tree.name = Symbol.FUNCTION.value
    return tree
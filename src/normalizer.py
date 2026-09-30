import ast
import builtins


BUILTIN_NAMES = frozenset(dir(builtins))

def should_preserve_name(name):
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

class Symbols:
    VARIABLE   = "VAR"
    ARGUMENT   = "ARG"
    ATTRIBUTE  = "ATTR"
    FUNCTION   = "FUNCTION_NAME"
    UNKNOWN    = "UNKN"


class Normalizer(ast.NodeTransformer):
    def __init__(self, function_name):
        super().__init__()
        
        self.function_name = function_name

        self.name_bindings = {
            Symbols.VARIABLE: {},
            Symbols.ARGUMENT: {},
            Symbols.ATTRIBUTE: {},
        }

        self.symbols_count = {
            Symbols.VARIABLE: 0,
            Symbols.ARGUMENT: 0,
            Symbols.ATTRIBUTE: 0,
        }


    def get_or_add(self, name, symbol_type):
        if name in self.name_bindings[symbol_type]:
            return self.name_bindings[symbol_type][name]

        new_binding = symbol_type + str(self.symbols_count[symbol_type])
        self.name_bindings[symbol_type][name] = new_binding
        self.symbols_count[symbol_type] += 1

        return new_binding


    def visit_Constant(self, node):
        if node.value != None:            
            node.value = LITERALS.get(type(node.value), Symbols.UNKNOWN)
        return node


    def visit_Name(self, node):
        if node.id == self.function_name:
            node.id = Symbols.FUNCTION
            return node

        if node.id in self.name_bindings[Symbols.ARGUMENT]:
            node.id = self.name_bindings[Symbols.ARGUMENT][node.id]
            return node

        if not should_preserve_name(node.id):
            node.id = self.get_or_add(node.id, Symbols.VARIABLE)

        return node


    def visit_arg(self, node):
        node.arg = self.get_or_add(node.arg, Symbols.ARGUMENT)
        return node


    def visit_Attribute(self, node):
        node.value = self.visit(node.value)
        return node



def normalize(tree):
    if not isinstance(tree, ast.AsyncFunctionDef) and not isinstance(tree, ast.FunctionDef):
        raise ValueError(type(tree))

    Normalizer(tree.name).visit(tree)
    tree.name = Symbols.FUNCTION
    return tree
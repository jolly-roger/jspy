import io

from js.wrappers.W_GlobalObject import W_GlobalObject

from js.jscode import ast_to_bytecode, JsCode
from js.astbuilder import parse_to_ast
from js.functions import JsGlobalCode

import js.builtins.interpreter
from js.builtins.object_space import object_space

from js.execution_context import GlobalExecutionContext


def load_file(filename):
    f = io.open(str(filename))
    src = f.readall()
    return src


class InterpreterConfig(object):
    def __init__(self, config={}):
        self.debug = config.get('debug', True)


class Interpreter(object):
    """Creates a js interpreter"""
    def __init__(self, config={}):
        self.config = InterpreterConfig(config)
        self.global_object = W_GlobalObject()
        object_space.global_object = self.global_object
        object_space.interpreter = self

        js.builtins.setup_builtins(self.global_object)
        js.builtins.interpreter.setup_builtins(self.global_object)

    def run_ast(self, ast):
        symbol_map = ast.symbol_map
        code = ast_to_bytecode(ast, symbol_map)
        
        return self.run(code)

    def run_src(self, src):
        ast = parse_to_ast(src)
        return self.run_ast(ast)

    def run(self, code, interactive=False):
        assert isinstance(code, JsCode)
        c = JsGlobalCode(code)

        ctx = GlobalExecutionContext(c, self.global_object)
        object_space.global_context = ctx

        result = c.run(ctx)
        return result.value

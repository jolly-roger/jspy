from js.wrappers.W_BasicFunction import W_BasicFunction


class W_FunctionConstructor(W_BasicFunction):
    def _to_string_(self):
        return u'function Function() { [native code] }'

    # 15.3.2.1
    def Call(self, args=[], this=None, calling_context=None):
        arg_count = len(args)
        _args = u''
        body = u''
        if arg_count == 0:
            pass
        elif arg_count == 1:
            body = args[0].to_string()
        else:
            first_arg = args[0].to_string()
            _args = first_arg
            k = 2
            while k < arg_count:
                next_arg = args[k - 1].to_string()
                _args = _args + u',' + next_arg
                k = k + 1
            body = args[k - 1].to_string()

        src = u'function (' + _args + u') { ' + body + u' };'

        ast = parse_to_ast(src)
        symbol_map = ast.symbol_map
        code = ast_to_bytecode(ast, symbol_map)
        # TODO hackish
        func = code.opcodes[0].funcobj

        scope = object_space.get_global_environment()
        strict = func.strict
        params = func.params()
        w_func = object_space.new_func(func, formal_parameter_list=params, scope=scope, strict=strict)
        return w_func

    # TODO
    def Construct(self, args=[]):
        return self.Call(args, this=None)
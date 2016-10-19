from js.put_property import put_property

from js.wrappers._w import _w
from js.wrappers.W_BasicFunction import W_BasicFunction
from js.wrappers.W__Object import W__Object
from js.wrappers.null import newnull


class W__Function(W_BasicFunction):
    _immutable_fields_ = ['_type_', '_class_', '_extensible_', '_scope_', '_params_[*]', '_strict_', '_function_']

    def __init__(self, function_body, formal_parameter_list=[], scope=None, strict=False):
        W_BasicFunction.__init__(self)
        self._function_ = function_body
        self._scope_ = scope
        self._params_ = formal_parameter_list
        self._strict_ = strict

        # 13.2 Creating Function Objects
        # 14.
        _len = len(formal_parameter_list)
        # 15.
        put_property(self, u'length', _w(_len), writable=False, enumerable=False, configurable=False)
        # 16.
        proto_obj = W__Object()
        # 17.
        put_property(proto_obj, u'constructor', self, writable=True, enumerable=False, configurable=True)
        # 18.
        put_property(self, u'prototype', proto_obj, writable=True, enumerable=False, configurable=False)

        if strict is True:
            raise NotImplementedError()
        else:
            put_property(self, u'caller', newnull(), writable=True, enumerable=False, configurable=False)
            put_property(self, u'arguments', newnull(), writable=True, enumerable=False, configurable=False)

    def _to_string(self):
        return self._function_.to_string()

    def code(self):
        return self._function_

    def formal_parameters(self):
        return self._params_

    def Call(self, args=[], this=None, calling_context=None):
        code = self.code()
        strict = self._strict_
        scope = self.scope()

        ctx = FunctionExecutionContext(code,
                                       argv=args,
                                       this=this,
                                       strict=strict,
                                       scope=scope,
                                       w_func=self)
        ctx._calling_context_ = calling_context

        res = code.run(ctx)

        assert isinstance(res, Completion)
        return res.value

    # 15.3.5.4
    def get(self, p):
        v = W_BasicObject.get(self, p)
        if p is u'caller' and isinstance(v, W__Function) and v.is_strict():
            raise JsTypeError(u'')
        return v

    def scope(self):
        return self._scope_

    def is_strict(self):
        return self._strict_
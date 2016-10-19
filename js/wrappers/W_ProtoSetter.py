from js.wrappers.root import W_Root


class W_ProtoSetter(W_Root):
    def is_callable(self):
        return True

    def Call(self, args=[], this=None, calling_context=None):
        if not isinstance(this, W_BasicObject):
            raise JsTypeError(u'')

        proto = args[0]
        this._prototype_ = proto
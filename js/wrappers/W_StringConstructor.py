from js.wrappers.W_BasicFunction import W_BasicFunction


class W_StringConstructor(W_BasicFunction):
    def Call(self, args=[], this=None, calling_context=None):
        arg0 = get_arg(args, 0, _w(u""))
        strval = arg0.to_string()
        return W_String(strval)

    def Construct(self, args=[]):
        return self.Call(args).ToObject()

    def _to_string_(self):
        return u'function String() { [native code] }'
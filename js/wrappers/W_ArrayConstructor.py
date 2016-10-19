from js.wrappers.W_BasicFunction import W_BasicFunction


class W_ArrayConstructor(W_BasicFunction):
    def __init__(self):
        W_BasicFunction.__init__(self)
        put_property(self, u'length', _w(1), writable=False, enumerable=False, configurable=False)

    def is_callable(self):
        return True

    def Call(self, args=[], this=None, calling_context=None):
        if len(args) == 1:
            _len = args[0]
            if isinstance(_len, W_Number):
                length = _len.ToUInt32()
                if length != _len.ToNumber():
                    raise JsRangeError()
                array = object_space.new_array(_w(length))
            else:
                length = 1
                array = object_space.new_array(_w(length))
                array._idx_put(0, _len, False)

            return array
        else:
            array = object_space.new_array()
            for index, obj in enumerate(args):
                array._idx_put(index, obj, False)
            return array

    def Construct(self, args=[]):
        return self.Call(args)
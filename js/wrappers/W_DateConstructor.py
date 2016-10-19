import time


from js.wrappers.W_BasicFunction import W_BasicFunction


class W_DateConstructor(W_BasicFunction):
    def Call(self, args=[], this=None, calling_context=None):
        #from js.builtins import get_arg
        # TODO
        #import datetime

        #if len(args) > 1:
        #    arg0 = get_arg(args, 0);
        #    arg1 = get_arg(args, 1, _w(0));
        #    arg2 = get_arg(args, 2, _w(0));

        #    year = arg0.ToInteger()
        #    month = arg1.ToInteger() + 1
        #    day = arg2.ToInteger() + 1

        #    d = datetime.date(year, month, day)
        #    sec = time.mktime(d.timetuple())
        #    value = _w(int(sec * 1000))

        #elif len(args) == 1:
        #    arg0 = get_arg(args, 0);
        #    if isinstance(arg0, W_String):
        #        raise NotImplementedError()
        #    else:
        #        num = arg0.ToNumber()
        #        if isnan(num) or isinf(num):
        #            raise JsTypeError(unicode(num))
        #        value = _w(int(num))
        #else:
        #    value = _w(int(time.time() * 1000))
        value = _w(int(time.time() * 1000))

        obj = object_space.new_date(value)
        return obj

    def Construct(self, args=[]):
        return self.Call(args).ToObject()

    def _to_string_(self):
        return u'function Date() { [native code] }'
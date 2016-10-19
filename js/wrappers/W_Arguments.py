from js.object_map import new_map

from js.wrappers.W__Object import W__Object


class W_Arguments(W__Object):
    _class_ = 'Arguments'

    def __init__(self, func, names, args, env, strict=False):
        W__Object.__init__(self)
        self.strict = strict
        _len = len(args)
        put_property(self, u'length', _w(_len), writable=True, enumerable=False, configurable=True)

        _map = W__Object()
        mapped_names = new_map()
        indx = _len - 1
        while indx >= 0:
            val = args[indx]
            put_property(self, unicode(str(indx)), val, writable=True, enumerable=True, configurable=True)
            if indx < len(names):
                name = names[indx]
                if strict is False and not mapped_names.contains(name):
                    mapped_names = mapped_names.add(name)
                    g = make_arg_getter(name, env)
                    p = make_arg_setter(name, env)
                    desc = PropertyDescriptor(setter=p, getter=g, configurable=True)
                    _map.define_own_property(unicode(str(indx)), desc, False)
            indx = indx - 1

        if not mapped_names.empty():
            self._paramenter_map_ = _map

        if strict is False:
            put_property(self, u'callee', _w(func), writable=True, enumerable=False, configurable=True)
        else:
            # 10.6 14 thrower
            pass
from js.builtins import get_arg
from js.object_space import w_return, _w


def setup(global_object):
    from js.builtins import put_native_function, put_property
    from js.jsobj import W_Console
    from js.object_space import object_space

    w_console = W_Console()
    object_space.assign_proto(w_console)
    put_property(global_object, u'console', w_console)
    
    put_native_function(w_console, u'log', log)


@w_return
def log(this, args):
    for arg in args:
        print arg.to_string()

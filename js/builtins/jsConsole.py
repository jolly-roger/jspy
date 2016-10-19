from js.builtins import get_arg
from js.object_space import w_return

from js.builtins import put_native_function
from js.builtins.object_space import object_space

from js.put_property import put_property

from js.wrappers._w import _w
from js.wrappers.W_Console import W_Console


def setup(global_object):
    w_console = W_Console()
    put_property(global_object, u'console', w_console)
    
    put_native_function(w_console, u'log', _log)
    put_native_function(w_console, u'dir', _dir)


@w_return
def _log(this, args):
    for arg in args:
        print arg.to_string()

@w_return
def _dir(this, args):
    dir(args[0])

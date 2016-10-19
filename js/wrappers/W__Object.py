from js.wrappers.null import newnull
from js.wrappers.W_BasicObject import W_BasicObject


class W__Object(W_BasicObject):
    def __init__(self):
        self._prototype_ = newnull()
    
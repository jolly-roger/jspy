from js.wrappers.primitive import W_Primitive


class W_Number(W_Primitive):
    """ Base class for numbers, both known to be floats
    and those known to be integers
    """
    _type_ = 'number'

    def ToObject(self):
        obj = object_space.new_number(self)
        return obj

    def to_boolean(self):
        num = self.ToNumber()
        if isnan(num):
            return False
        return bool(num)

    def __eq__(self, other):
        if isinstance(other, W_Number):
            return self.ToNumber() == other.ToNumber()
        else:
            return False
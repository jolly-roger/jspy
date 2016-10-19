class W_Root(object):
    _settled_ = True
    _immutable_fields_ = ['_type_']
    _type_ = ''

    def __str__(self):
        return self.to_string()

    def to_string(self):
        return u''

    def type(self):
        return self._type_

    def to_boolean(self):
        return False

    def ToPrimitive(self, hint=None):
        return self

    def ToObject(self):
        raise JsTypeError(u'W_Root.ToObject')

    def ToNumber(self):
        return 0.0

    def ToInteger(self):
        num = self.ToNumber()
        if num == NAN:
            return 0
        if num == INFINITY or num == -INFINITY:
            raise Exception('dafuq?')
            return 0

        return int(num)

    def ToInt32(self):
        num = self.ToInteger()
        #if num == NAN or num == INFINITY or num == -INFINITY:
            #return 0

        return int32(num)

    def ToUInt32(self):
        num = self.ToInteger()
        #if num == NAN or num == INFINITY or num == -INFINITY:
            #return 0
        return uint32(num)

    def ToInt16(self):
        num = self.ToInteger()
        #if num == NAN or num == INFINITY or num == -INFINITY or num == 0:
            #return 0

        return uint16(num)

    def is_callable(self):
        return False

    def check_object_coercible(self):
        pass
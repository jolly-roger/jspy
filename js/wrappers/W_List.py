from js.wrappers.root import W_Root


class W_List(W_Root):
    def __init__(self, values):
        self.values = values

    def to_list(self):
        return self.values

    def __str__(self):
        return 'W_List(%s)' % (unicode([unicode(v) for v in self.values]))
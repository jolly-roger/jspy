class PyObj(object):
    def __init__(self, pyobj):
        self._pyobj = pyobj
    
    def getObj(self):
        return self._pyobj
    
    def to_string(self):
        return unicode(dir(self._pyobj))

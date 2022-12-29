class Context:
    def __init__(self, parent: 'Context' = None) -> None:
        self.parent = parent
        self.children = list()
        self.module = None
        self.func = None
        self.block = None
        self.globals = dict()
        self.variables = dict()

    def addChild(self) -> 'Context':
        child = Context(self)
        child.module = self.module
        child.func = self.func
        child.block = self.block
        child.globals = self.globals
        if self.func is not None:
            child.variables = self.variables.copy()
        self.children.append(child)
        return child

    def __repr__(self) -> str:
        if self.block:
            return repr(self.block)
        elif self.func:
            return repr(self.func)
        elif self.module:
            return repr(self.module)
        else:
            return '<Undefined context>'

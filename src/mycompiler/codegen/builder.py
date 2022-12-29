import llvmlite.ir as ll


wrapped_func = [
    'alloca',
    'store',
    'branch',
    'cbranch',
    'ret',
    'ret_void',
]


class Builder(ll.IRBuilder):
    def checkBlockEnd(self, func):
        def wrapped(*args, **kwargs):
            if not self.block.is_terminated:
                return func(*args, **kwargs)
        return wrapped
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for attr in wrapped_func:
            if hasattr(self, attr) and callable(getattr(self, attr)):
                setattr(self, attr, self.checkBlockEnd(getattr(self, attr)))

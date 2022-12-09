class IteratorWrapper:
    def __init__(self, iterable, endToken=None):
        self.iterator = iter(iterable)
        self.endToken = endToken
        self.update()

    def update(self):
        try:
            self.next = next(self.iterator)
        except StopIteration:
            self.next = self.endToken

    def empty(self):
        return self.next is self.endToken

    def peek(self):
        return self.next

    def pop(self):
        ret = self.next
        self.update()
        return ret

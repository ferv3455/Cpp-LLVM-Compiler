class IteratorWrapper:
    def __init__(self, iterable):
        self.iterator = iter(iterable)
        self.update()

    def update(self):
        try:
            self.next = next(self.iterator)
        except StopIteration:
            self.next = None

    def empty(self):
        return self.next is None

    def peek(self):
        return self.next

    def pop(self):
        ret = self.next
        self.update()
        return ret

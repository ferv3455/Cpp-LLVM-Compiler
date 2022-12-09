class Item:
    def __init__(self, a) -> None:
        self.a = a

    def __hash__(self) -> int:
        return hash(self.a)

    def __eq__(self, __o: object) -> bool:
        return self.a == __o.a


b = dict()
b[Item(1)] = 2
print(b[Item(1)])
print(b)

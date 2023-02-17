import string, random

# from abstract.vector import Vector

def generateID():
    id = ""
    prefixID = "#"
    lengthID = 12
    random_source = string.ascii_uppercase + string.digits

    for i in range(lengthID):
        id += random.choice(random_source)

    id_list = list(id)
    id = "".join(id_list)
    return f"{prefixID}{id}"


class Vector2D:
    def __init__(self, x, y, id=generateID()) -> None:
        self.dx: float = 0.0
        self.dy: float = 0.0
        self.dx = x
        self.dy = y
        self.id = id

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.dx},{self.dy})"

p = Vector2D(1,2)
print(p)
print(p.id)
# print()

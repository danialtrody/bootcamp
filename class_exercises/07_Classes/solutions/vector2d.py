class Vector2D:

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Vector2D({self.x},{self.y})"

    def __repr__(self) -> str:
        return f"Vector2D({self.x},{self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return False

        return self.x == other.x and self.y == other.y

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        return Vector2D(self.x * scalar, self.y * scalar)

    def __abs__(self) -> float:
        return self.magnitude()

    def magnitude(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def dot(self, other: "Vector2D") -> float:
        return self.x * other.x + self.y * other.y

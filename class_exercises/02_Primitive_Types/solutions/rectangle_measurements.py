width: float = float(input("Enter the width of the rectangle: "))
height: float = float(input("Enter the height of the rectangle: "))

area: float = width * height
perimeter: float = 2 * (width + height)
diagonal: float = (width**2 + height**2)**0.5

print(f"Width: {width}")
print(f"Height: {height}")
print(f"Area: {area}")
print(f"Perimeter: {perimeter}")
print(f"Diagonal: {round(diagonal,2)}")
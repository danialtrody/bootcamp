def solve_quadratic(a: float, b: float, c: float) -> str:
    first_x = (-b - (b**2 - 4 * a * c) ** 0.5) / (2 * a)
    second_x = (-b + (b**2 - 4 * a * c) ** 0.5) / (2 * a)

    return f"x1 = {first_x:.2f}, x2 = {second_x:.2f}"

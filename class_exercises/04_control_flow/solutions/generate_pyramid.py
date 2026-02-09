def generate_pyramid(height: int) -> str:
    
    if height < 1:
        raise ValueError("Height must be at least 1.")
    
    if height > 9:
        raise ValueError("Height cannot exceed 9.")

    lines = []

    for i in range(1, height + 1):
        left = ''.join(str(n) for n in range(1, i + 1))
        right = left[:-1][::-1]
        spaces = ' ' * (height - i)
        lines.append(spaces + left + right)

    return '\n'.join(lines)




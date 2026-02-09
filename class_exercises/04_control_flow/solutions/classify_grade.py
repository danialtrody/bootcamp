def classify_grade(score: int) -> str:
    
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100.")

    if 90 <= score <= 100:
        return "A"
    elif 80 <= score <= 89:
        return "B"
    elif 70 <= score <= 79:
        return "C"
    elif 60 <= score <= 69:
        return "D"
    else:  
        return "F"

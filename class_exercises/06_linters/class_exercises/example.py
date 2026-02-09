"""
Example module to demonstrate the power of linters and formatters.
This code intentionally violates many best practices!
"""

def calculate_test_statistics(scores):
    """
    Calculate statistics for a list of test scores.

    This function takes a list of test scores and calculates various statistics
    including the average score, highest and lowest scores, and counts how many
    students passed or failed.

    Purpose:
        Help teachers quickly analyze test results to understand class performance.
        A passing score is 60 or above.

    Parameters:
        scores: A list of numbers representing test scores (0-100 scale)

    Returns:
        A dictionary with the following keys:
        - 'average': The average (mean) score
        - 'highest': The highest score
        - 'lowest': The lowest score
        - 'passed': Number of scores >= 60
        - 'failed': Number of scores < 60
        - 'pass_rate': Percentage of students who passed

    Example:
        >>> scores = [75, 82, 55, 90, 68]
        >>> result = calculate_test_statistics(scores)
        >>> print(result['average'])
        74.0
    """
    t = 0
    c = 0
    p = 0
    f = 0
    h = 0
    l = 100

    for s in scores:
        if s >= 0 and s <= 100:
            t = t + s
            c = c + 1
            if s > h:
                h = s
            if s < l:
                l = s
            if s >= 60:
                p = p + 1
            else:
                f = f + 1

    if c > 0:
        a = t / c
        pr = (p / c) * 100
    else:
        a = 0
        pr = 0
        h = 0
        l = 0

    return {'average': a, 'highest': h, 'lowest': l, 'passed': p, 'failed': f, 'pass_rate': pr}


# Example usage
if __name__ == '__main__':
    test_scores = [81]

    result = calculate_test_statistics(test_scores)
    print("Test Statistics:")
    print(f"  Average Score: {result['average']:.1f}")
    print(f"  Highest Score: {result['highest']}")
    print(f"  Lowest Score: {result['lowest']}")
    print(f"  Students Passed: {result['passed']}")
    print(f"  Students Failed: {result['failed']}")
    print(f"  Pass Rate: {result['pass_rate']:.1f}%")

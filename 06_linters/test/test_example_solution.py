from solution.example_solution import calculate_test_statistics


def test_statistics_valid_scores():
    
    assert calculate_test_statistics([85, 92, 78, 45, 88, 67, 95, 54, 73, 81]) == \
        {'average': 75.8, 'highest': 95, 'lowest': 45,
         'passed': 8, 'failed': 2, 'pass_rate': 80.0}
        
def test_statistics_single_score():
 
    assert calculate_test_statistics([81]) == \
       {'average': 81.0, 'highest': 81, 'lowest': 81,
        'passed': 1, 'failed': 0, 'pass_rate': 100.0}
       
def test_statistics_empty_list():
 
    assert calculate_test_statistics([]) == \
      {'average': 0, 'highest': 0, 'lowest': 0,
       'passed': 0, 'failed': 0, 'pass_rate': 0}
      
def test_statistics_all_failed():
    
    assert calculate_test_statistics([50, 49, 20, 1, 0, 10, 5, 43, 33, 21]) == \
        {'average': 23.2, 'highest': 50, 'lowest': 0,
         'passed': 0, 'failed': 10, 'pass_rate': 0.0}
        
def test_statistics_all_passed():
    
    assert calculate_test_statistics([60, 69, 70, 81, 80, 100, 75, 93, 83, 91]) == \
        {'average': 80.2, 'highest': 100, 'lowest': 60,
         'passed': 10, 'failed': 0, 'pass_rate': 100.0}
        
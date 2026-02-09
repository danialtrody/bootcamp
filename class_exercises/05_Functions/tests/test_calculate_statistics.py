import pytest
from solutions.calculate_statistics import calculate_statistics

def test_calculate_statistics_normal_and_empty():
    
    output1 = {
        'temperatures': {'sum': 95.0, 'average': 23.75, 'min': 22.5, 'max': 25.0},
        'humidity': {'sum': 255, 'average': 63.75, 'min': 60, 'max': 68}
    }
    
    output2 = {
        'temperatures': {'sum': None, 'average': None, 'min': None, 'max': None},
        'humidity': {'sum': None, 'average': None, 'min': None, 'max': None}
    }
    
    assert calculate_statistics(
        temperatures=[22.5, 24.0, 23.5, 25.0],
        humidity=[60, 65, 62, 68]
        ) == output1
    
    assert calculate_statistics(
        temperatures=[],
        humidity=[]
        ) == output2

def test_calculate_statistics_single_value():
    output = {
        'temperatures': {'sum': 50, 'average': 50, 'min': 50, 'max': 50},
        'humidity': {'sum': 50, 'average': 50, 'min': 50, 'max': 50}
    }
    
    assert calculate_statistics(
        temperatures=[50],
        humidity=[50]
    ) == output

        
    
    
    

def test_calculate_statistics_no_input():
    with pytest.raises(ValueError, match="No datasets provided."):
        calculate_statistics()
    
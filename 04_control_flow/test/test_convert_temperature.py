import pytest
from solution.convert_temperature import convert_temperature

def test_convert_temperature():
    assert convert_temperature(0, "C", "F") == 32.0
    assert convert_temperature(100, "C", "K") == 373.15
    assert convert_temperature(32, "F", "C") == 0.0
    assert convert_temperature(0, "C", "C") == 0.0
    

    
def test_convert_temperature_invalid_unit():
    with pytest.raises(ValueError, match="Invalid unit. Use 'C', 'F', or 'K'."):
        convert_temperature(0, "A", "C")
    with pytest.raises(ValueError, match="Invalid unit. Use 'C', 'F', or 'K'."):
        convert_temperature(0, "C", "A")

    
def test_convert_temperature_negative_kelvin():
    with pytest.raises(ValueError, match="Kelvin cannot be negative."):
        convert_temperature(-1, "K", "C")
        
    
def test_convert_temperature_below_absolute_zero():
    with pytest.raises(ValueError, match="Temperature below absolute zero."):
        convert_temperature(-274.15, "C", "C")


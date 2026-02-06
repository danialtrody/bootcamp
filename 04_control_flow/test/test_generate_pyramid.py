import pytest
from solutions.generate_pyramid import generate_pyramid


def test_generate_pyramid():
    assert generate_pyramid(3) ==  (
                                    "  1\n"
                                    " 121\n"
                                    "12321"
                                    )



def test_generate_pyramid_invalid_low():
    with pytest.raises(ValueError, match="Height must be at least 1."):
        generate_pyramid(0)
        
        

def test_generate_pyramid_invalid_high():
    with pytest.raises(ValueError, match="Height cannot exceed 9."):
        generate_pyramid(10)
        
        
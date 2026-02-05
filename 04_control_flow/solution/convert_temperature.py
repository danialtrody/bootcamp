def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    
    if from_unit != 'C' and from_unit != 'F' and from_unit != 'K':
        raise ValueError("Invalid unit. Use 'C', 'F', or 'K'.")
    
    if to_unit != 'C' and to_unit != 'F' and to_unit != 'K':
        raise ValueError("Invalid unit. Use 'C', 'F', or 'K'.")
    
    if from_unit == 'K' and value < 0:
        raise ValueError("Kelvin cannot be negative.")
    
    if from_unit == 'C' and value < -273.15:
       raise ValueError("Temperature below absolute zero.")
   
    if from_unit == to_unit:
        return value
    
    if from_unit == 'C' and to_unit == 'F':
        return value * 9 / 5 + 32
    
    if from_unit == 'F' and to_unit == 'C':
        return (value - 32) * 5/9
    
    if from_unit == 'C' and to_unit == 'K':
        return value + 273.15
    
    if from_unit == 'K' and to_unit == 'C':
        return value - 273.15
    
    if from_unit == "F" and to_unit == "K":
        return (value - 32) * 5/9 + 273.15
    
    if from_unit == "K" and to_unit == "F":
        return (value - 273.15) * 9/5 + 32
       

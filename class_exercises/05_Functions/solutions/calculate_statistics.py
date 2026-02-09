from typing import Dict,List,Optional

def calculate_statistics(**kwargs: List[float]) -> Dict[str, Dict[str ,Optional[float]]]:
    
    if not kwargs:
        raise ValueError("No datasets provided.")
    
    statistics = {}
    
    for statistic_name, data in kwargs.items():
        
        if not data :
            statistics[statistic_name] = {"sum":None,
                                          "average":None,
                                          "min":None,
                                          "max":None} 
            
        else:    
            statistic_sum = sum(data )
            statistic_average = statistic_sum/len(data)
            statistic_min = min(data )
            statistic_max = max(data )
            
            statistics[statistic_name] = {"sum":statistic_sum,
                                        "average":statistic_average,
                                        "min":statistic_min,
                                        "max":statistic_max} 
    return statistics

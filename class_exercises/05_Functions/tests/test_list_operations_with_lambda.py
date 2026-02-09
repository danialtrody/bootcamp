from solutions.list_operations_with_lambda import filter_adults , get_names ,sort_by_age


people = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 17},
    {"name": "Charlie", "age": 30},
    {"name": "Diana", "age": 16}
]

empty_list = []

single_person = [{"name": "Alice", "age": 25}]



def test_filter_adults():
    assert filter_adults(people) == \
    [{'name': 'Alice', 'age': 25}, {'name': 'Charlie', 'age': 30}]
    
    assert filter_adults(empty_list) == []
    
    assert filter_adults(single_person) == [{"name": "Alice", "age": 25}]

    
    
def test_get_names():
    assert get_names(people) == \
    ['Alice', 'Bob', 'Charlie', 'Diana']
    
    assert get_names(empty_list) == []
    
    assert get_names(single_person) == ["Alice"]


    
def test_sort_by_age():
    assert sort_by_age(people) == \
    [{'name': 'Diana', 'age': 16}, {'name': 'Bob', 'age': 17}, 
    {'name': 'Alice', 'age': 25}, {'name': 'Charlie', 'age': 30}]  
    
    assert sort_by_age(empty_list) == []

    assert sort_by_age(single_person) == [{"name": "Alice", "age": 25}]

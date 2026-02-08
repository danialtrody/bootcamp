def filter_adults(people: list[dict]) -> list[dict]:
    
    return list(filter(lambda person: person["age"] >=18, people))


def get_names(people: list[dict]) -> list[str]:
    
    return list(map(lambda person: person["name"], people))


def sort_by_age(people: list[dict]) -> list[dict]:
    
    return list(sorted(people, key=lambda person: person["age"]))




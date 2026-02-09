from solution.exercise2 import extract_title

def test_extract_title():
    html = "<html><head><title>My Title</title></head><body></body></html>"
    assert extract_title(html) == "My Title"
    
def test_title_with_spaces():
    html = "<html><head><title>   Title with spaces   </title></head></html>"
    assert extract_title(html) == "   Title with spaces   "
    
def test_title_with_nested_tags():
    html = "<html><head><title>Nested <b>Title</b></title></head></html>"
    assert extract_title(html) == "Nested <b>Title</b>"

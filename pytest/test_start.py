def test_numbers_equal():
    a = 1 + 1
    b = 2
    assert a == b
    
def test_value_in_list():
    li = ("a", "b", "c")
    assert "d" in li
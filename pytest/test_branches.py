def a(number):
    if (number % 2 == 0):
        return "even"
    else:
        return "odd"

def b(number):
    if (number % 2 == 0):
        return "even"


def test_a():
    assert "even" == a(2)
    
def test_b():
    assert "even" == b(2)
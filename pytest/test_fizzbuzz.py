import pytest

def fizz_buzz(value):
    if(value % 3 == 0 and value % 5 == 0):
        return "FizzBuzz"
    elif (value % 3 == 0):
        return "Fizz"
    elif(value % 5 == 0):
        return "Buzz"
    else:
        return value

 
@pytest.mark.parametrize("input", [3,6,9,12,18,21,24,27,33,36,39,42,48])  
# @pytest.mark.parametrize("input", [3,6,9,12,18,21,24,27,30,33,36,39,42,45,48])  
def test_multiples_of_3_return_Fizz(input):    
    assert "Fizz" == fizz_buzz(input)
    
@pytest.mark.parametrize("input", [15,30,45])  
def test_multiples_of_3_and_5_return_FizzBuzz(input):    
    assert "FizzBuzz" == fizz_buzz(input)
    
@pytest.mark.parametrize("input", [5,10,20,25,35,40,50])  
def test_multiples_of_5_return_Buzz(input):    
    assert "Buzz" == fizz_buzz(input)
    
@pytest.mark.parametrize("input", [1,2,4,7,8,11,13,14,16,17,19,22,23,26,28,29,31,32,34,37,38,41,43,44,46,47,49])  
def test_otherwise_returns_input(input):    
    assert input == fizz_buzz(input)
    
    
@pytest.mark.parametrize("input, expected",
                         [(1, 1),
                          (2, 2),
                          (3, "Fizz"),
                          (4, 4),
                          (5, "Buzz"),
                          (15,"FizzBuzz")])
def test_multiple_inputs(input, expected):
    assert expected == fizz_buzz(input)
    print(f"{input}: {expected}")
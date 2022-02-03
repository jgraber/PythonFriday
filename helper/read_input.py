# https://docs.python.org/dev/library/functions.html#input
var = input("Please enter something: ")
print("You entered: " + var)


# https://docs.python.org/dev/library/getpass.html
import getpass
password = getpass.getpass("Please enter your password: ")
print(f"You entered {len(password)} characters")
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 401 | 403:
            return "Not allowed"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something is wrong with the internet"  

        
print(http_error(400))
print(http_error(500))

print(http_error(401))
print(http_error(403))


# ----------------------------------------------

def classify_number(n):
    match n:
        case x if x < 0:
            return f"negative: {x}"
        case 0:
            return "zero"
        case x if x > 0:
            return f"positive: {x}"


print(classify_number(-10))
print(classify_number(0))
print(classify_number(23))

# ----------------------------------------------


def handle_event(event):
    match event:
        case {"type": "user_created", "user_id": user_id}:
            print(f"User created: {user_id}")

        case {"type": "user_deleted", "user_id": user_id}:
            print(f"User deleted: {user_id}")

        case _:
            print("Unknown event")


handle_event({"type": "user_created", "user_id": 11, "email": "info@..."})
handle_event({"type": "user_deleted", "user_id": 6, "date": "2026-01-02 16:19:29"})

# ----------------------------------------------

def parse_coordinates(value):
    match value:
        case [x, y]:
            return f"2D point: {x}, {y}"
        case [x, y, z]:
            return f"3D point: {x}, {y}, {z}"
        case _:
            return "Invalid coordinates"

print(parse_coordinates((1)))
print(parse_coordinates((1,2)))
print(parse_coordinates((1,2,3)))
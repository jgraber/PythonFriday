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



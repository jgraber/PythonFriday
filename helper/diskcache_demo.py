from diskcache import Cache

cache = Cache("./.cache")  # pick a folder for cached results

@cache.memoize(expire=3)           # note the parentheses
def factorial(n):
    print(f"***{n}***")
    return n * factorial(n-1) if n else 1

print(factorial(5))
print(factorial(6))
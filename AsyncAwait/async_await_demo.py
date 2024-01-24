import asyncio
import time


async def hi():
    print("Hello")
    await asyncio.sleep(1)
    print("World")


async def sequence():
    await hi()
    await hi()
    await hi()

start = time.perf_counter()
asyncio.run(sequence())
elapsed = time.perf_counter() - start
print(f"sequence() executed in {elapsed:0.2f} seconds.")

print("*" * 50)

# https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently
async def parallel():
    await asyncio.gather(hi(), hi(), hi())

asyncio.run(parallel())    
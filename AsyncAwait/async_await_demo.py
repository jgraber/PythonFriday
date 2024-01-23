import asyncio


async def hi():
    print("Hello")
    await asyncio.sleep(1)
    print("World")


async def sequence():
    await hi()
    await hi()
    await hi()

asyncio.run(sequence())

print("*" * 50)

# https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently
async def parallel():
    await asyncio.gather(hi(), hi(), hi())

asyncio.run(parallel())    
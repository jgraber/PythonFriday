import asyncio
import time


async def use_sleep():
    print("start sleep")
    time.sleep(2)
    print("end sleep")


asyncio.run(use_sleep())

# async def use_sleep():
#     await time.sleep(2)

# asyncio.run(use_sleep())
# # => TypeError: object NoneType can't be used in 'await' expression


async def hi():
    print("Hello")
    await asyncio.sleep(1)
    # time.sleep(1)
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

start = time.perf_counter()
asyncio.run(parallel())  
elapsed = time.perf_counter() - start
print(f"parallel() executed in {elapsed:0.2f} seconds.")  


print("*" * 50)

async def too_long():
    await asyncio.sleep(10)

# https://docs.python.org/3/library/asyncio-task.html#timeouts
async def starter():
    try:
        async with asyncio.timeout(5):
            await too_long()
    except TimeoutError:
        print("Got a time out for the long running method")

start = time.perf_counter()
asyncio.run(starter()) 
elapsed = time.perf_counter() - start
print(f"starter() executed in {elapsed:0.2f} seconds.") 

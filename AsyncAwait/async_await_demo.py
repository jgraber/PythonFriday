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

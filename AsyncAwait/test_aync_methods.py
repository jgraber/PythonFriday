import asyncio

import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_function():
    await asyncio.sleep(1)

@pytest_asyncio.fixture()
async def prepare():
    print("setup...")
    await asyncio.sleep(1)

@pytest.mark.asyncio
async def test_function_with_fixture(prepare):
    await asyncio.sleep(1)

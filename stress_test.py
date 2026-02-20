import asyncio
import aiohttp
import time
import random
import string
from typing import List

BASE_URL = "http://localhost:8000"
MAX_CONCURRENT = 50
connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT)


def random_string(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def random_email() -> str:
    return f"{random_string(8)}@example.com"


def random_name() -> str:
    first = random.choice(["John", "Jane", "Bob", "Alice", "Charlie", "Diana"])
    last = random.choice(["Smith", "Doe", "Johnson", "Williams", "Brown", "Jones"])
    return f"{first} {last}"


async def create_user(session: aiohttp.ClientSession) -> dict:
    try:
        user_data = {
            "email": random_email(),
            "username": random_string(12),
            "full_name": random_name(),
            "password": "testpass123"
        }
        async with session.post(f"{BASE_URL}/users/", json=user_data) as resp:
            return {"status": resp.status, "data": await resp.json() if resp.status == 201 else None}
    except Exception as e:
        return {"status": 0, "error": str(e)}


async def create_bulk_users(session: aiohttp.ClientSession, count: int) -> dict:
    try:
        users = [
            {
                "email": random_email(),
                "username": random_string(12),
                "full_name": random_name(),
                "password": "testpass123"
            }
            for _ in range(count)
        ]
        async with session.post(f"{BASE_URL}/users/bulk", json=users) as resp:
            if resp.status == 201:
                return {"status": resp.status, "data": await resp.json()}
            return {"status": resp.status, "data": 0}
    except Exception as e:
        return {"status": 0, "error": str(e)}


async def stress_test_single(concurrent: int, total: int):
    print(f"\n=== Stress Test: {total} single user creations ({concurrent} concurrent) ===")
    
    async with aiohttp.ClientSession(connector=connector) as session:
        start = time.time()
        
        tasks = [create_user(session) for _ in range(total)]
        results = await asyncio.gather(*tasks)
        
        elapsed = time.time() - start
        
        success = sum(1 for r in results if r.get("status") == 201)
        failed = total - success
        errors = sum(1 for r in results if r.get("status") == 0)
        
        print(f"Total time: {elapsed:.2f}s")
        print(f"Requests/sec: {total/elapsed:.2f}")
        print(f"Success: {success}, Failed: {failed}, Errors: {errors}")


async def stress_test_bulk(batches: int, batch_size: int):
    print(f"\n=== Stress Test: {batches} bulk creates ({batch_size} users each) ===")
    
    async with aiohttp.ClientSession(connector=connector) as session:
        start = time.time()
        
        tasks = [create_bulk_users(session, batch_size) for _ in range(batches)]
        results = await asyncio.gather(*tasks)
        
        elapsed = time.time() - start
        
        total_users = batches * batch_size
        success = sum(len(r.get("data") or []) for r in results if r.get("status") == 201)
        failed = total_users - success
        
        print(f"Total time: {elapsed:.2f}s")
        print(f"Users/sec: {total_users/elapsed:.2f}")
        print(f"Success: {success}, Failed: {failed}")


async def main():
    print("Starting PostgreSQL Stress Test")
    print("=" * 40)
    
    await stress_test_single(concurrent=20, total=100)
    
    await stress_test_bulk(batches=5, batch_size=50)
    
    await stress_test_single(concurrent=30, total=200)
    
    print("\n=== Stress Test Complete ===")


if __name__ == "__main__":
    asyncio.run(main())

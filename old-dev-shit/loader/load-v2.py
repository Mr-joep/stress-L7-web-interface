import aiohttp
import asyncio
from aiohttp import ClientSession, TCPConnector

async def fetch(url, session):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Error: {e}")

async def bound_fetch(sem, url, session):
    async with sem:
        return await fetch(url, session)

async def main():
    file_path = 'request_website.txt'

    try:
        with open(file_path, 'r') as file:
            url = file.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return

    concurrency_limit = 200  # Adjust the concurrency limit for performance
    requests_per_iteration = 200  # Adjust the number of requests per loop iteration

    sem = asyncio.Semaphore(concurrency_limit)

    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        while True:
            tasks = [bound_fetch(sem, url, session) for _ in range(requests_per_iteration)]
            await asyncio.gather(*tasks)
            # Add any additional logic as needed

if __name__ == '__main__':
    asyncio.run(main())

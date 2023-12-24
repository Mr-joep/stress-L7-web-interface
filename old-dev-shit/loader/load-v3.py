import asyncio
import aiohttp

async def fire_and_forget(url, session, counter):
    try:
        async with session.get(url) as response:
            # You can add some minimal processing here if needed
            pass
        counter.increment()
    except Exception as e:
        print(f"Error: {e}")

class RequestCounter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        with open("test.txt", "w") as file:
            file.write(f"Total requests: {self.count}\n")

async def main():
    file_path = 'request_website.txt'

    try:
        with open(file_path, 'r') as file:
            url = file.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return

    requests_per_iteration = 100  # Adjust the number of requests per loop iteration
    counter = RequestCounter()

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        while True:
            tasks = [fire_and_forget(url, session, counter) for _ in range(requests_per_iteration)]
            await asyncio.gather(*tasks)
            await asyncio.sleep(0)  # Allow other tasks to run

if __name__ == '__main__':
    asyncio.run(main())

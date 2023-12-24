import asyncio
import aiohttp
import os

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

    def reset(self):
        current_count = self.count
        self.count = 0
        return current_count

def get_log_file_path(log_folder, base_name="test.txt"):
    log_file_path = os.path.join(log_folder, base_name)
    if os.path.exists(log_file_path):
        # If the file already exists, find the next available number
        file_number = 1
        while os.path.exists(os.path.join(log_folder, f"{base_name}-{file_number}.txt")):
            file_number += 1
        log_file_path = os.path.join(log_folder, f"{base_name}-{file_number}.txt")
    return log_file_path

async def write_requests_per_second(counter):
    log_folder = "requests_log"
    os.makedirs(log_folder, exist_ok=True)

    while True:
        await asyncio.sleep(1)
        total_requests = counter.reset()
        log_file_path = get_log_file_path(log_folder)
        with open(log_file_path, "w") as file:
            file.write(f"Requests per second: {total_requests}\n")

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
        asyncio.create_task(write_requests_per_second(counter))
        
        while True:
            tasks = [fire_and_forget(url, session, counter) for _ in range(requests_per_iteration)]
            await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())

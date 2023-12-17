import aiohttp
import asyncio
import time
import os

async def check_website_once(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                print(f"Website {url} is online.")
    except aiohttp.ClientError as e:
        print(f"Website {url} is down. Error: {e}")

async def make_request(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return 1
    except aiohttp.ClientError:
        return 0

async def monitor_website(url, max_concurrent_requests=50):
    start_time = time.time()
    request_count = 0

    # Create 'requests_log' folder if it doesn't exist
    if not os.path.exists('requests_log'):
        os.makedirs('requests_log')

    # Find the next available log file name
    log_file_name = os.path.join('requests_log', 'requests_log-1.txt')
    count = 1
    while os.path.exists(log_file_name):
        count += 1
        log_file_name = os.path.join('requests_log', f"requests_log-{count}.txt")

    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=max_concurrent_requests)) as session:
            while True:
                tasks = [make_request(session, url) for _ in range(max_concurrent_requests)]
                request_count += sum(await asyncio.gather(*tasks))

                time_elapsed = time.time() - start_time
                if time_elapsed >= 1:
                    with open(log_file_name, "a") as file:
                        file.write(f"Requests per second: {request_count / time_elapsed:.2f}\n")
                    start_time = time.time()
                    request_count = 0

    except KeyboardInterrupt:
        pass

    total_time = time.time() - start_time
    average_requests_per_second = request_count / total_time if total_time > 0 else 0
    with open(log_file_name, "a") as file:
        file.write(f"\nAverage requests per second: {average_requests_per_second:.2f}\n")

if __name__ == "__main__":
    website_url = "http://192.168.154.139"

    # Step 1: Check if the website is online
    asyncio.run(check_website_once(website_url))

    # Step 2 and 3: Monitor the website indefinitely with increased concurrent requests
    asyncio.run(monitor_website(website_url, max_concurrent_requests=1))

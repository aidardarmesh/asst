import asyncio
import requests

# Synchronous blocking function
def blocking_http_call():
    print("Sending HTTP request")
    response = requests.get('http://google.com')
    print(f"Got HTTP response with status {response.status_code}")

async def main():
    print("Started async main")

    # Start a concurrent async task for demonstration
    async def counter():
        for i in range(5):
            print(f"Async working {i}")
            await asyncio.sleep(0.5)

    # Schedule async counter task
    task = asyncio.create_task(counter())

    # Run the blocking call in default thread pool executor
    blocking_http_call()
    # await asyncio.get_running_loop().run_in_executor(None, blocking_http_call)

    # Wait for the counter task to complete
    await task

asyncio.run(main())

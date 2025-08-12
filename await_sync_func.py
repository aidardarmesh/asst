import asyncio

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

async def main():
    n = 5
    result = await asyncio.to_thread(factorial, n)
    print(f"Factorial of {n} is {result}")

if __name__ == "__main__":
    asyncio.run(main())
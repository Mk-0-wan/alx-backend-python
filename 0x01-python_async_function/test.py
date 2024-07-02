import asyncio
from previous_file import wait_random

async def wait_n(n: int, max_delay: int) -> list:
    tasks = [asyncio.create_task(wait_random(max_delay)) for _ in range(n)]
    delays = []
    
    for task in asyncio.as_completed(tasks):
        delay = await task
        # Insert delay into the sorted position in the list
        insert_sorted(delays, delay)
    
    return delays

def insert_sorted(delays: list, delay: float):
    if not delays:
        delays.append(delay)
        return
    for i in range(len(delays)):
        if delay < delays[i]:
            delays.insert(i, delay)
            return
    delays.append(delay)

# Example usage
if __name__ == "__main__":
    n = 5
    max_delay = 10
    delays = asyncio.run(wait_n(n, max_delay))
    print(delays)


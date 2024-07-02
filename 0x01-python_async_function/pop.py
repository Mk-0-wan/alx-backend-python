#!/usr/bin/env python3
"""Making multiple co-routine objects"""
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random

def fix_array(arry: list, elem: float):
    """Inserts elem into arry maintaining ascending order"""
    if not arry:
        arry.append(elem)
        return
    for idx in range(len(arry)):
        if elem < arry[idx]:
            arry.insert(idx, elem)
            return
    arry.append(elem)

async def wait_n(n: int, max_delay: int) -> list:
    """Making multiple concurrency co-routine"""
    # make a list of all the co-routines returned
    tasks = [asyncio.create_task(wait_random(max_delay)) for _ in range(n)]
    await_list = []
    # append to the list all the early task completed in the tasks routine
    for task in asyncio.as_completed(tasks):
        finished = await task
        fix_array(await_list, finished)

    return await_list

if __name__ == "__main__":
    print(asyncio.run(wait_n(5, 5)))

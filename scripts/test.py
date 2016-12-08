import sys
import time

import asyncio

async def backgroundFutur():
    await asyncio.sleep(5)
    print("fetching some data after")
    await asyncio.sleep(5)
    return "backgrounb"
def foregroundData():
    print("fetching some data now")
    yield "foreground"
def testAsync():
    print("getting some data eh ...")
    for data in foregroundData():
        yield(data)
    yield asyncio.get_event_loop().run_until_complete(backgroundFutur())
if __name__ == "__main__":
    # print("asdasd")
    # for data in testAsync():
    #     print(data)
    import json
    data = {"asd":["asd","asd"],"asd2":("1","2","3")}
    print(json.dumps(data))
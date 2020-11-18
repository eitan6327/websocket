#!/usr/bin/env python3

# Echo server. Will reverse everything we throw at it.

import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        #await websocket.send(message[::-1])
        print(message)

loop = asyncio.get_event_loop()
loop.run_until_complete(websockets.serve(echo, 'localhost', 8765))
loop.run_forever()
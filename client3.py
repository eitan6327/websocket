#!/usr/bin/env python3

# Client. Sends stuff from STDIN to the server.

import asyncio
import websockets

async def hello(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello world!")
        async for message in websocket:
            print(message)
            await websocket.send(input())

asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8765'))
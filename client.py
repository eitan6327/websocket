#!/usr/bin/env python

# WS client example

import asyncio
import websockets

async def hello():
	uri = "ws://localhost:8764"

	async with websockets.connect(uri) as websocket:
	
		msg = input("MESSEGE: ")

		# await websocket.send('HF92B0201;0;02;00\n')
		await websocket.send(msg)

		print(f"> {msg}")

		rx = await websocket.recv()
		print(f"< {rx}")



asyncio.get_event_loop().run_until_complete(hello())

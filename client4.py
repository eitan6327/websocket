#!/usr/bin/env python3

# Client. Sends stuff from STDIN to the server.

import asyncio
import websockets
from time import sleep

class MSG:
	pass



PROD_ID = MSG()
PROD_ID.data = 'HF92B0101;0;01;00\n'
PROD_ID.time = 20

PROD_GUI = MSG()
PROD_GUI.data = 'HF92B0101;0;02;00\n'
PROD_GUI.time = 50

msg_list = (PROD_ID, PROD_GUI)

async def hello(uri):
    async with websockets.connect(uri) as websocket:
    	t = 0

    	await websocket.send(msg_list[0].data)
    	await asyncio.sleep(0.01)
    	while True:
    		
    		
    		async for message in websocket:
    			if message:
    				print(message)
    			sent_f = False

    			for i in range(len(msg_list)):
    				if (t % msg_list[i].time) == 0:
    					if True:
    						await websocket.send(msg_list[i].data)
    						sent_f = True
    			if sent_f == False:
    				await websocket.send('')

    			t += 1

	    		await asyncio.sleep(.2)

asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8765'))
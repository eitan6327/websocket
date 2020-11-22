#!/usr/bin/env python3

# Client. Sends stuff from STDIN to the server.

import asyncio
import websockets
from time import sleep
import time
from datetime import datetime

# Create a message class
class MSG:
	pass



PROD_ID = MSG()
PROD_ID.data = 'HF92B0101;0;01;00\n'
# message delay
PROD_ID.time = 0.1
# total number if messages to send
PROD_ID.count = 3

PROD_GUI = MSG()
PROD_GUI.data = 'HF92B0101;0;02;00\n'
# message delay
PROD_GUI.time = 10 
# total number if messages to send
PROD_GUI.count = 0

PROD_LIST = MSG()
PROD_LIST.data = 'HF92B0101;0;04;00\n'
# message delay
PROD_LIST.time = 3
# total number if messages to send
PROD_LIST.count = 2

# list of messages
msg_list = (PROD_ID, PROD_GUI, PROD_LIST)

async def msg_send(msg, websocket):
    e = msg.count
    while e:
        await websocket.send(msg.data)
        e -= 1 
        if e:
            await asyncio.sleep(msg.time)

async def msg_rec(websocket):
    while True:
        async for message in websocket:
            # generate a time stamp for received message
            tim = (f"RX time: {time.strftime('%X')}.")
            a = (time.time())
            a = str(int((a - int(a)) * 1000))
            tim = (f"RX time: {time.strftime('%X')}." + a)
            print(tim)
            print(message)
            # time interval for checking the receive buffer
            await asyncio.sleep(0.01)

async def hello(uri):
    #start a WebSocket connection
    async with websockets.connect(uri) as websocket:
        # send all the messages
        req0 = asyncio.create_task(
            msg_send(PROD_ID, websocket))

        req1 = asyncio.create_task(
            msg_send(PROD_LIST, websocket))

        req2 = asyncio.create_task(
            msg_send(PROD_GUI,websocket)
        )
        # Receive messages
        rec_task = asyncio.create_task(
            msg_rec(websocket))
        # wait fot alt the transmits to complete
        await req0
        await req1
        await req2
        rec_task

 

# Change the localhost to match the IP of the ESP32
asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8765'))
#!/usr/bin/env python3

# Client. Sends stuff from STDIN to the server.

import asyncio
import websockets
from time import sleep
import time
from datetime import datetime
import socket
import pickle

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
PROD_GUI.count = 1

PROD_LIST = MSG()
PROD_LIST.data = 'HF92B0101;0;04;00\n'
# message delay
PROD_LIST.time = 2
# total number if messages to send
PROD_LIST.count = 5

# list of messages
msg_list = (PROD_ID, PROD_GUI, PROD_LIST)


def getTime():
    tim = (f"RX time: {time.strftime('%X')}.")
    a = (time.time())
    a = str(int((a - int(a)) * 1000))
    tim = (f"{time.strftime('%X')}." + a)
    return(tim)
 
    

async def msg_send(msg, websocket):
    e = msg.count
    while e:
        # Print the time stamp for sent message
        print('TX time: ' + getTime())
        print('    ' + msg.data)
        await websocket.send(msg.data)
        e -= 1 
        if e:
            await asyncio.sleep(msg.time)

async def msg_rec(websocket):
    while True:
        async for message in websocket:
            # Print the time stamp for received message
            print('RX time: ' + getTime())
            print(message)
            # time interval for checking the receive buffer
            await asyncio.sleep(0.01)

async def main(uri):
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

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(local_ip)


existing_ip = ''
try:
    file = open("ip.pkl", "rb")
    existing_ip = pickle.load(file)
    #file.close()
    print('existing ip: ' + existing_ip)
except:
    print('no valid file')

new_ip_read = input('enter server "ip:port" or <enter> to accept ' + str(existing_ip) + ': ')
new_ip_read = new_ip_read.replace(' ','')
if new_ip_read == '':
    new_ip_read = existing_ip
ip_format_valid = True
new_ip = new_ip_read.split(':')
new_ip[0] = new_ip[0].split('.')
if len(new_ip) !=2 or len(new_ip[0]) != 4:
    ip_format_valid = False
    
elif new_ip[1].isnumeric() == False:
    ip_format_valid = False
elif int(new_ip[1]) > 65535:
    ip_format_valid = False

else:
    for item in new_ip[0]:
        if item.isnumeric() == False:
            ip_format_valid = False
            break
        if  int(item) > 255:
            ip_format_valid = False
            break
    
if ip_format_valid == False:
    print('Bad ip:port format......Exiting')
    exit()    
else:
    print('good format')

if new_ip_read == '':
    new_ip_read = existing_ip
else:
    file = open('ip.pkl', 'wb')
    pickle.dump(new_ip_read, file)
    file.close()

print(new_ip_read)
print('ws://' + new_ip_read)


asyncio.get_event_loop().run_until_complete(main('ws://' + new_ip_read))
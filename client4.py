#!/usr/bin/env python3

# Client. Sends stuff from STDIN to the server.

import asyncio
import websockets
from time import sleep
import time
from datetime import datetime
import socket
import pickle
import logging

# Create a message class
class MSG:
	pass

PROD_2APP = MSG()
PROD_2APP.data = 'HF92B0301;0;01;00\n'
PROD_2APP.time = 2
PROD_2APP.count = 1

PROD_ID = MSG()
PROD_ID.data = 'HF92B0101;0;01;00\n'
# message delay
PROD_ID.delay = .1
# time between messages
PROD_ID.time = 0.1
# total number if messages to send
PROD_ID.count = 0

PROD_GUI = MSG()
PROD_GUI.data = 'HF92B0101;0;02;00\n'
# message delay
PROD_GUI.delay = 0.5
# time between messages
PROD_GUI.time = 10 
# total number if messages to send
PROD_GUI.count = 1

PROD_LIST = MSG()
PROD_LIST.data = 'HF92B0101;0;04;00\n'
# message delay
PROD_LIST.time = 2
# total number if messages to send
PROD_LIST.count = 0

PROD_MON = MSG()
PROD_MON.data = 'HF92B0201;0;01;00\n'
PROD_MON.time = .2
PROD_MON.delay = .1
PROD_MON.count = 10

# list of messages
msg_list = (PROD_2APP, PROD_ID, PROD_GUI, PROD_LIST, PROD_MON)

async def msg_send(msg, websocket):
    e = msg.count
   
    try:
        await asyncio.sleep(msg.delay)
    except:
        pass
    while e:
        log(f'Request to server:\n{msg.data}')
        await websocket.send(msg.data)
        e -= 1 
        if e:
            await asyncio.sleep(msg.time)

async def msg_rec(websocket):
    while websocket.connection_open:
        async for message in websocket:
            log(f'Response from server:\n{message}')
            # time interval for checking the receive buffer
            await asyncio.sleep(0.01)

async def main(uri):
    #start a WebSocket connection
    async with websockets.connect(uri) as websocket:
        # send all the messages
        req = []

        for item in msg_list:
            req.append(asyncio.create_task(
                msg_send(item, websocket)))

        # Receive messages
        rec_task = asyncio.create_task(
            msg_rec(websocket))
        # wait fot alt the transmits to complete
        for item in req:
            await item
        # End the program if there is nothing to send
        rec_task
        await asyncio.sleep(1)


def get_server_ip_port():
    ''' 
    This routine reads the last ip:port from file and prompts the user to update it 
    The enter key prompt the function to use the old ip:port
    '''
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
    return new_ip_read


if __name__ == "__main__":
    format = "%(asctime)s.%(msecs)03d: %(message)s"
    logging.basicConfig(format = format, level = logging.INFO,
    datefmt = "%H:%M:%S")

    log = logging.info
    log("Main : starting")

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print('local ip: ', local_ip)

    serv_ip_port = get_server_ip_port()

    print('ws://' + serv_ip_port)
    for i in range(3):
        asyncio.get_event_loop().run_until_complete(main('ws://' + serv_ip_port))

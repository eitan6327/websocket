
# WS server example

import asyncio
import websockets
import threading

import serial
import serial.tools.list_ports as port_list
from time import sleep
from time import time


def read_buffer(ser):
        temp = 1
        lines2 = b''
        lines = read_serial(ser)
        while len(lines) != 0:
        	lines2 = lines2 + lines
        	lines = read_serial(ser)
        return lines2



def read_serial(ser):
	lines = b''
	while True:
		while ser.in_waiting:
			line = ser.readline()
			lines = lines + line
			#print(line)
			#ser.write(line.encode('utf-8'))
		sleep(0.01)
		if ser.in_waiting == False:
			break
	return lines


async def hello(websocket, path):
    msg = await websocket.recv()

    msg = msg

    print(msg)

    s_msg = 'HF92B0201;0;02;00\n'

    #ser.write(msg.encode('utf-8'))

    val = read_serial(ser)


    print(val.decode('utf-8'))

    rx_msg = f"RX MSG: {msg}"
 
    # await websocket.send(val.decode('utf-8'))
    await websocket.send(rx_msg)
    print(f"> {rx_msg}")

async def echo(websocket, path):
    async for message in websocket:
        #await websocket.send(message[::-1])
        print('From MSD View: ', message)
        ser.write(message.encode('utf-8'))

        val = read_serial(ser)
        print(val.decode('utf-8'))

        rx_msg = f"RX MSG: {val}"
        #print(f"> {rx_msg}")
        await websocket.send(val.decode('utf-8'))


def thread_function(server_loop):
	i = 0
	while i < 10:
		i += 1
		print('Thread', i)
		sleep(0.1)
		




if __name__ == "__main__":

	p_open = False
	tries = 1

	print('starting...')

	while p_open == False:
	        start = time()
	        pp = port_list.comports()
	        
	        elapse = time() - start
	        print(elapse)
	        ports = list(pp)
	        p_list = []
	        com_select = ''
	        for p in ports:
	                p_list.append(p)                
	                print(p)
	                #print((str(p).split(' ')[2]) == 'USB')
	                #find the highest value com port
	                if ((str(p).split(' ')[2]) == 'USB'):
	                        com_select = str(p).split(' ')[0]
	                        print(f'com selected: {com_select}')

	        
	        if com_select == '' :
	                print('Exiting: No COM Port Found')
	                quit()

	        # print (port_list)
	        com = com_select
	        while p_open == False:
		        try:
		                ser = serial.Serial(com, timeout=1)
		                print(f'Connected to: {ser.name}')
		                p_open = True
		        except:
		                tries = tries + 1
		                print(f'trying {tries}')
		                sleep(.05)
	
	x = threading.Thread(target=thread_function, args=(1,))
	x.start()

	loop = asyncio.get_event_loop()
	loop.run_until_complete(websockets.serve(echo, 'localhost', 8765))
	loop.run_forever()


	'''

	start_server = websockets.serve(hello, "localhost", 80)

	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()
	'''
	

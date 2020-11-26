
# WS server example

import asyncio
import websockets
import threading
import socket

import serial
import serial.tools.list_ports as port_list
from time import sleep
from time import time
import logging
from det_com import detect_com_ports as com

port = '8765'

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


async def echo(websocket, path):
	print(dir(websocket))
	async for message in websocket:
		#await websocket.send(message[::-1])
		log(f'From Client: {websocket.remote_address[0]}')
		print(message)
		ser.write(message.encode('utf-8'))

		val = read_serial(ser)
		if(val != ''):
			log('Serial Response:')
			print(val.decode('utf-8'))

			try:
				await websocket.send(val.decode('utf-8'))
			except:
				print('rx error')


if __name__ == "__main__":
	format = "%(asctime)s.%(msecs)03d: %(message)s"
	logging.basicConfig(format = format, level = logging.INFO,
	datefmt = "%H:%M:%S")

	log = logging.info
	log("Main : starting")
	# detect the USB com port
	ser = com()

	hostname = socket.gethostname()
	local_ip = socket.gethostbyname(hostname)
	print('Point Client to:', local_ip + ':' + port)


	loop = asyncio.get_event_loop()
	loop.run_until_complete(websockets.serve(echo, local_ip, port))
	loop.run_forever()


	

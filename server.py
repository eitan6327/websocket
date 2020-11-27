
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
		if ser.in_waiting == False:
			break
	return lines


async def echo(websocket, path):
	async for message in websocket:
		log(f'From Client: {websocket.remote_address[0]}')
		print(message)
		vala = read_serial(ser)
		valb = b''
		while (vala != b''):
			valb += vala
			sleep(0.003)

			log(f'Serial Response P:\n{vala.decode("utf-8")}')
			vala = read_serial(ser)
		ser.write(message.encode('utf-8'))
		sleep(0.01)
		val = read_serial(ser)
		if (valb + val != b''):
			log(f'Serial Response:\n{val.decode("utf-8")}')
			val = valb + val
			try:
				await websocket.send(val.decode('utf-8'))
			except:
				log(f'ws send error {val.decode("utf-8")}')
				break


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


	

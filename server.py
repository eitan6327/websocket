
# WS server example

import asyncio
import websockets
import threading
import socket

import serial
# import serial.tools.list_ports as port_list
from time import sleep
from time import time
import logging
# from det_com import detect_com_ports as com
from ports_open import InitializePorts, IdentifyPortThread

port = '8765'

global last_read_time
last_read_time = 0

def read_serial(ser):
	lines = b''
	if ser.in_waiting:
		lines = ser.read_all()
	#if ser.in_waiting == False:
	#	break
	return lines

async def do_st(websocket):
	global ser_valid
	send_valid = True
	while send_valid:
		val = b''
		if send_valid:
			if ser_valid:
				try:
					val = read_serial(ser)
				except Exception as e:
					log('error serial read')
					ser_valid = False
		if val != b'':
			global last_read_time
			last_read_time = time()
			log(f'Serial Response:\n{val.decode("utf-8")}')
			try:
				await websocket.send(val.decode('utf-8'))
			except Exception as e:
				send_valid = False

		await asyncio.sleep(0.01)
	print('Done with websocket')
		
async def find_serial():
	while True:
		global ser_valid
		global ser
		if ser_valid == False:
			ser_list = []
			ser_list = fp.getValidSerials()
			if len(ser_list):
				ser = ser_list[0]
				ser_valid = True
				print('serial connected')
		await asyncio.sleep(0.5)


# async def setup_serial():
# 	await find_serial

async def main(websocket, path):
	'''
	ser_list = fp.getValidSerials()
	if len(ser_list):
		ser = ser_list[0]
		ser_valid = True
	print('lenth of serial', len(ser_list))
	'''
	global ser_valid
	ser_valid = False
	validate_port = asyncio.create_task(find_serial())
	read_serial = asyncio.create_task(do_st(websocket))
	
	try:
		async for message in websocket:
			log(f'From Client: {websocket.remote_address[0]}\n{message}')
		
			try:
				global ser
				global last_read_time
				# log(f'last_read_time: {last_read_time}')
				delta = time() - last_read_time
				#TODO: Figure out why we need a delay here
				while time() - last_read_time < 0.01:
					# log('start delay')
					await asyncio.sleep(.005)
				# log(f'end delay delta: {time() - last_read_time}')
				ser.write(message.encode('utf-8'))
			except Exception as e:
				if ser_valid == True:
					log(f"error serial write {message.encode('utf-8')}")
					ser_valid = False

		# await validate_port
		await validate_port
		await read_serial
	except:
		print('Done with Websocket')
		pass


if __name__ == "__main__":
	format = "%(asctime)s.%(msecs)03d: %(message)s"
	logging.basicConfig(format = format, level = logging.INFO,
	datefmt = "%H:%M:%S")

	log = logging.info
	log("Main : starting")
	# detect the USB com port
	#ser = com()
	fp = InitializePorts().run()
	# ser_list = []
	global ser_valid
	ser_valid = False


	# find_serial()

	
	#IdentifyPortThread

	hostname = socket.gethostname()
	local_ip = socket.gethostbyname(hostname)
	print('Point Client to:', local_ip + ':' + port)


	loop = asyncio.get_event_loop()
	for i in range(3):
		try:
			loop.run_until_complete(websockets.serve(main, local_ip, port))
			loop.run_forever()
			print('Normal Exit')
			break
		except Exception as e:
			print(str(e))
			print('retry: ', i)
			sleep(3)

	print('Exiting....')

	


	

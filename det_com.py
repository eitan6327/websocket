
import serial
import serial.tools.list_ports as port_list
from time import sleep
from time import time
import logging


def detect_com_ports():
	p_open = False
	tries = 1


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
		            ser = serial.Serial(com, timeout=1, baudrate=921600)
		            print(f'Connected to: {ser.name}')
		            ser.reset_input_buffer()
		            p_open = True
		    except:
		            tries = tries + 1
		            print(f'trying {tries}')
		            sleep(.05)
		return ser


if __name__ == "__main__":
	format = "%(asctime)s.%(msecs)03d: %(message)s"
	logging.basicConfig(format = format, level = logging.INFO,
	datefmt = "%H:%M:%S")

	log = logging.info
	log("Main : starting")

	print(detect_com_ports())

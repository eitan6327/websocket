import threading
import time 
import serial
import serial.tools.list_ports as port_list
import logging




class DetectPortThread(threading.Thread):
	def __init__(self, args=(), kwargs=None):
		threading.Thread.__init__(self, args=(), kwargs=None)
		self.daemon = True
		self.receive_messages = args

	def run(self):
		self.port_set = set()
		while True:
			pp = port_list.comports()
			
			p_list = []
			com_select = []
			new_port_set = set()
			for p in pp:
				p_list.append(p)                
				#print(p)
				if ((str(p).split(' ')[2]) == 'USB'):
				        com_select.append(str(p).split(' ')[0])
				        new_port_set.add(str(p).split(' ')[0])
			self.port_set = new_port_set
			# print('port_set', self.port_set, '\nlenth of set', len(self.port_set))


	'''
	def do_thing_with_message(self, message):
		if self.receive_messages:
			print (threading.currentThread().getName(), (message))
	'''

	def get_serial_ports(self):
		return self.port_set

class IdentifyPortThread(threading.Thread):
	def __init__(self, args=(), kwargs=None):
		threading.Thread.__init__(self, args=(), kwargs=None)
		self.daemon = True
		self.receive_messages = args
		self.open_ports = set()

	def run(self):
		ser = {}
		
		while True:

			ports = self.receive_messages.get_serial_ports()
			# print('Available Ports', self.open_ports)
			for port in ports:
				if port not in self.open_ports:
					try:
						ser[port] = serial.Serial(port, timeout=1, baudrate=921600, rtscts = True)
						self.open_ports.add(port)
						log(f'added: {port}')
						#ser[port].close()

					except:
						log(f'failed adding port {port}')
					
			ser_to_remove = set()
			for port in self.open_ports:
				try:
					ser[port].write('HF92B0101;0;01;00\n'.encode("utf-8"))
					time.sleep(0.1)
					val = (ser[port].read_all())
					log(f'{port} RX:\n{val.decode("utf-8")}')
					
				except:
					ser_to_remove.add(port)
					log(f'removed: {port}')
					

			for port in ser_to_remove:
				self.open_ports.remove(port)
				log(f'final removal: {port}')
			
			time.sleep(1)

	def getAvailablePorts(self):
		return self.open_ports

class InitializePorts:
	def __init__(self):
		pass

	def run(self):

		# This thread detects all the USB ports and updates the ports set
		self.t = DetectPortThread(args='0p',)
		self.t.start()
		# This Thread identify the ability to write and read from the ports and creates a set
		self.s = IdentifyPortThread(args=self.t,)
		self.s.start()

	def AvailablePorts(self):
		return self. s.getAvailablePorts()

	



if __name__ == '__main__':
	format = "%(asctime)s.%(msecs)03d: %(message)s"
	logging.basicConfig(format = format, level = logging.INFO,
	datefmt = "%H:%M:%S")
	log = logging.info

	ports = InitializePorts()
	ports.run()
	while True:
		time.sleep(1)
		
		
		print(f'Available Ports: {ports.AvailablePorts()}')
		pass


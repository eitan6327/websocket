import threading
import time 
import serial
import serial.tools.list_ports as port_list
import logging




class DetectPortThread(threading.Thread):
	def __init__(self, args=(), kwargs=None):
		threading.Thread.__init__(self, args=(), kwargs=None)
		self.daemon = True

	def run(self):
		self.port_set = set()
		while True:
			pp = port_list.comports()
			
			com_select = []
			new_port_set = set()
			for p in pp:
 
				if ((str(p).split(' ')[2]) == 'USB'):
				        com_select.append(str(p).split(' ')[0])
				        new_port_set.add(str(p).split(' ')[0])
			self.port_set = new_port_set
			time.sleep(0.1)
 
	def get_serial_ports(self):
		return self.port_set

class IdentifyPortThread(threading.Thread):
	def __init__(self, args=(), kwargs=None):
		threading.Thread.__init__(self, args=(), kwargs=None)
		self.daemon = True
		self.port_detect_thread = args
		self.existing_ports = set()
		self.inuse_ports = set()
		self.valid_ports = set()

	def run(self):
		ser = {}
		
		while True:
			ports = self.port_detect_thread.get_serial_ports()
			ports_to_remove = set()
			for port in self.valid_ports:
				if port not in ports:
					ports_to_remove.add(port)

			for port in ports_to_remove:
				self.valid_ports.remove(port)
				log(f'removed  valid port: {port}')
	
			open_ports = set()
			for port in ports:
				if port not in self.valid_ports:
					try:

						ser[port] = serial.Serial(port, timeout=1, baudrate=921600, rtscts = True)
						open_ports.add(port)
						if port in self.inuse_ports:
							self.inuse_ports.remove(port)
						# log(f'added open port: {port}')
					except:
						if port not in self.inuse_ports:
							log(f'port {port} is in use')
						self.inuse_ports.add(port)
						# close the port since the port may have been already assigned
						try:
							ser[port].close()
						except:
							pass

						
			# validating the product in the port
			for port in open_ports:
				try:
		
					ser[port].write('HF92B0101;0;01;00\n'.encode("utf-8"))
					time.sleep(0.01)
					val = (ser[port].readline())
					log(f'{port} RX:\n{val.decode("utf-8")}')
					if self.validateMessage(val) == 'OK':
						self.valid_ports.add(port)
					else:
						log('bad data')
					
				except:
					pass


			time.sleep(1)

	def getAvailablePorts(self):
		return self.valid_ports

	def validateMessage(self, msg):
		if len (msg) < 9:
			return 'Failed'
		msg = msg.decode("utf-8")
		msg = msg[:-1]
		# check for and remove CR
		if msg[-1:] == '\r':
			msg = msg[:-1]
		# validate the checksum
		cs = int(msg[-2:],16)
		i = msg[:-2].encode("utf-8")
		for l in i:
			cs = l + cs
		if msg[:1] == 'H' and cs & 0xFF == 0:
			return 'OK'
		else:
			return 'Fail'



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

	ports_to_print = set()
	while True:
		time.sleep(1)
		
		get_ports = ports.AvailablePorts()
		if ports_to_print != get_ports:
			ports_to_print = set()
			for i in get_ports:
				ports_to_print.add(i)

			print(f'Available Ports: {ports_to_print}')

			
		


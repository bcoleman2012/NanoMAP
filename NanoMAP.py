import time
import sys
import serial
import serial.tools.list_ports
from threading import Thread

# SessionManager provides an interface for string-based messages and the arduino device
# NanoMAPController provides interface for scripting support
# gcode-style input files will be supported by NanoMAPController

class SessionManager: 
	""" Simple wrapper class for an Arduino serial connection session """
	def __init__(self, verbose = False, selected_port = None): 
		self._verbose = verbose
		self._arduino_ports = []
		self._arduino_serial_session = None
		self._selected_port = selected_port
		self._serial_session = None
		if self._verbose: 
			print "SessionManager verbose mode activated" 

	def scanPorts(self): 
		if self._verbose: 
			for p in serial.tools.list_ports.comports():
				print p

		self._arduino_ports = [p.device for p in serial.tools.list_ports.comports() if 'Arduino' in p.description]
		
		if len(self._arduino_ports) == 1:
			self._selected_port = self._arduino_ports[0]

		elif (len(self._arduino_ports) <= 0): 
			print "Error: Arduino device not found. Are you using a knockoff?"
			knockoff = raw_input("(Y/N):")
			if knockoff.strip().lower() == "y":
				print "Select a device from the following list:"
				for p in serial.tools.list_ports.comports():
					print "Device:",p.device,"\tDescription:",p.description
				comport = raw_input("Enter the selected device (as shown above): ")
				self._arduino_ports = [p.device for p in serial.tools.list_ports.comports() if comport.lower() in p.description.lower()]
				self._selected_port = self._arduino_ports[0]

			elif knockoff.strip().lower() == "n":
				print "Please check to ensure that the Arduino device is attached."
		else: 
			print "Multiple Arduino devices found. Choose a device from the list: "
			for p in serial.tools.list_ports.comports():
				if 'Arduino' in p.description: 
					print "Device:",p.device,"\tDescription:",p.description
			comport = raw_input("Enter the selected device (as shown above): ")
			for p in self._arduino_ports: 
				if comport.lower() in p.lower(): 
					self._selected_port = p
					if self._verbose: 
						print "Connected with selected port:",self._selected_port


	def initSession(self, baudrate = 9600): 
		if (self._selected_port is not None): 

			start_indicator = "r" # needs replaced with better code in next firmware iteration
			
			if self._verbose: 
				print "Attempting serial connection with Arduino device on",self._selected_port
			
			self._serial_session = serial.Serial(self._selected_port, baudrate, timeout = 0.1)
			timeout = 10
			start_time = time.time()

			if self._verbose: 
				print "Serial connection established, attempting firmware handshake"

			'''
			curr_time = time.time()
			while (curr_time < start_time + timeout) and (self._serial_session.readline() != start_indicator):
				curr_time = time.time()

			if curr_time > start_time + timeout: 
				if self._verbose: 
					print "Unable to communicate with device. Is the firmware up to date?" 
			'''
		else: 
			self.scanPorts()

			# next time I have access, implement useful verbose logs for timeout reached and success condition
			# for some reason the following hangs: 
			# 	if (self._serial_session.readline() == start_indicator): 
			# 		if self._verbose: 
			# 			print "Successful connection established with device at " + self._selected_port
			# 		return
			# if self._verbose: 
			# 	print "Unable to make a connection. Timeout exceeded or device not found."

	def write(self, message): 
		if self._serial_session is None: 
			return
		if self._verbose: 
			print "Sending message: ", message
		self._serial_session.write(message)

	def readline(self): 
		data = self._serial_session.readline()
		if self._verbose: 
			print "Received: ", data
		return data

	def sendCommand(self, command): 
		""" This method implements the wait function for the script. Expects newline at end of command"""
		endStepIndicator = "EXIT\n"
		self.write(command)
		while (self.readline() != endStepIndicator): 
			if self._verbose: 
				print '*', 
		if self._verbose: 
			print "\nExecuted cmd: ",command 


class NanoMAPController: 
	""" Interface class between the SessionManager and the script input. Construct with a valid, connected SessionManager"""
	def __init__(self, session_manager): 
		self._session_manager = session_manager
		self._script = []

	def parseScriptFromFile(self, filename): 
		infile = open(filename, 'r')
		for cmd in infile:
			if ('#' not in cmd) and (cmd != "\n"): 
				if cmd[-1] != '\n': 
					cmd = cmd + '\n'
				self._script.append(cmd)

	def checkCommand(self,cmd): 
		""" checks if command is valid """
		return True

	def script(self): 
		for cmd in self._script: 
			self._session_manager.sendCommand(cmd)

	def parseScriptFromList(self, cmd_list): 
		for cmd in script_list: 
			self._session_manager.sendCommand(cmd)


def runOnPort(port, portList):
	sessionManager = SessionManager(verbose = False, selected_port = port)
	sessionManager.initSession()

	interfaceController = NanoMAPController(sessionManager)
	interfaceController.parseScriptFromFile("cmd.txt")
	interfaceController.script()
	try:
		portList.remove(port)
	except ValueError: 
		pass

if __name__ == "__main__":

	ports = [p.device for p in serial.tools.list_ports.comports()]
	if len(ports) > 1: 
		# if we have multiple devices attached, break out a separate thread for each one
		threads = []
		used_ports = []
		all_ports = serial.tools.list_ports.comports()
		while(True):

			if len(used_ports)>=len(all_ports): 
				continue

			print "Unused devices detected. Would you like to start a new actuation? (CTRL+C to exit)"
			user_response = raw_input("(Y/N): ")

			if user_response.strip().lower() == "y":
				all_ports = serial.tools.list_ports.comports()
				for p in all_ports: 
					if p.device not in used_ports: 
						print "Device:",p.device,"\tDescription:",p.description
				comport = raw_input("Enter the selected device (as shown above): ")
				for p in all_ports: 
					if comport.lower() in p.device.lower(): 
						print "Starting actuation on port",p
						used_ports.append(p.device)
						threads.append(Thread(target=runOnPort, args=(p.device, used_ports)))
						threads[-1].start()




	elif len(ports) == 1:
		# if we have only one devie attached, then don't worry about it
		sessionManager = SessionManager(verbose = False)
		sessionManager.scanPorts()
		sessionManager.initSession()

		interfaceController = NanoMAPController(sessionManager)
		interfaceController.parseScriptFromFile("cmd.txt")
		interfaceController.script()

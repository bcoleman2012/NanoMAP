import time
import sys
import serial
import serial.tools.list_ports

# SessionManager provides an interface for string-based messages and the arduino device
# NanoMAPController provides interface for scripting support
# gcode-style input files will be supported by NanoMAPController

class SessionManager: 
	""" Simple wrapper class for an Arduino serial connection session """
	def __init__(self, verbose = False): 
		self._verbose = verbose
		self._arduino_ports = []
		self._arduino_serial_session = None
		self._selected_port = None
		self._serial_session = None
		if self._verbose: 
			print "SessionManager verbose mode activated"

	def scanPorts(self): 
		if self._verbose: 
			for p in serial.tools.list_ports.comports():
				print p

		self._arduino_ports = [p.device for p in serial.tools.list_ports.comports() if 'Arduino' in p.description]
		if ((len(self._arduino_ports) == 0) and self._verbose): 
			print "Error: Arduino device not found"

	def initSession(self, baudrate = 9600): 
		if (len(self._arduino_ports) != 0): 
			self._selected_port = self._arduino_ports[0]

			start_indicator = "r" # needs replaced with better code in next firmware iteration
			
			if self._verbose: 
				print "Attempting serial connection with Arduino device on",self._selected_port
			
			self._serial_session = serial.Serial(self._selected_port, baudrate, timeout = 0.1)
			timeout = 10
			start_time = time.time()

			if self._verbose: 
				print "Serial connection established, attempting firmware handshake"

			while (time.time() < start_time + timeout) and (self._serial_session.readline() != start_indicator):
				pass

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



if __name__ == "__main__":
	sessionManager = SessionManager(verbose = True)
	sessionManager.scanPorts()
	sessionManager.initSession()

	interfaceController = NanoMAPController(sessionManager)
	interfaceController.parseScriptFromFile("cmd.txt")
	interfaceController.script()

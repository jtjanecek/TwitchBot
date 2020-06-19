import socket
import select
import sys	 
import time
import logging
import threading
import os
from datetime import datetime
from datetime import timedelta

class TwitchChatBot():
	def __init__(self, settings, plugins):
		''' Initializes the socket and the Bot
		'''

		self._socket_in_lock = threading.Lock()
		self._socket_in_queue = []
		self._socket_out_lock = threading.Lock()
		self._socket_out_queue = []

		# Setup object variables
		self._command_char = settings["command_char"]
		self._bytes_to_read = 512
		self._port = 6667
		self._host = "irc.twitch.tv" 
		self._nick = settings["nick"]
		self._pass = settings["oauth"]
		self._stream_to_watch = settings["stream"]
		self._plugins = plugins

		logging.info("Settings: {}".format(settings))

		self.connect()

		self.run_forever()

	def run_forever(self):
		while True:
			with self._socket_in_lock:
				if len(self._socket_in_queue) != 0:
					user, msg = self.get_user_and_message(self._socket_in_queue.pop())
					if user and msg:
						logging.info("{}: {}".format(user, msg))
						self.pass_to_plugins(user, msg)
			for plugin in self._plugins:
				msgs = plugin.get_outbound()
				if msgs != []:
					for msg in msgs:
						self.send_msg(msg)
			# If we get disconnected, reconnect
			time.sleep(.05)

	def pass_to_plugins(self, user, msg):
		for plugin in self._plugins:
			plugin.parse(user, msg)

	def connect(self):
		# Connect the socket
		self._socket = socket.socket()
		self._socket.settimeout(1)
		logging.info("SYS: Created Socket")
	
		self._socket.connect((self._host,self._port))
		logging.info("SYS: Connected socket to " + str(self._host) + ":" + str(self._port))

		PASS_S = "PASS " + self._pass + "\r\n"
		self._socket.send(PASS_S.encode())
	
		NICK_S = "NICK " + self._nick.lower() + "\r\n"
		self._socket.send(NICK_S.encode())

		JOIN_S = "JOIN #" + self._stream_to_watch + "\r\n"
		self._socket.send(JOIN_S.encode())

		logging.info("SYS: Initializing...")
		'''buf = self._socket.recv(self._bytes_to_read).decode()
		while "End of" not in buf:
			buf = self._socket.recv(self._bytes_to_read).decode()
		'''
		logging.info("SYS: Ready.")
		logging.info("SYS: Starting bot...")

		# Start read thread			
		self._t1 = threading.Thread( target = self._read_socket)
		self._t1.daemon = True
		self._t1.start()

		# Start write thread
		self._t2 = threading.Thread( target = self._write_socket)
		self._t2.daemon = True
		self._t2.start()

		self._t3 = threading.Thread( target = self._send_pings)
		self._t3.daemon = True
		self._t3.start()

	def _send_pings(self) -> None:
		t = datetime.now()
		while True:
			if datetime.now() > t + timedelta(seconds=30):
				with self._socket_out_lock:
					self._socket_out_queue.insert(0, "PING :tmi.twitch.tv")
				t = datetime.now()
			time.sleep(.01)

	def _read_socket(self) -> None:
		''' Continuously read the socket for messages
		'''
		ping_recv = True
		while True:
			with self._socket_in_lock:
				'''
				try:
					ready_to_read, ready_to_write, in_error = select.select([self._socket,], [self._socket,], [], 5)
				except select.error:
					logging.error("SOCKET CLOSED!")
				logging.info("{},{},{}".format(ready_to_read, ready_to_write, in_error))
				'''
				try:
					readbuf = self._socket.recv(self._bytes_to_read).decode().strip()
					logging.debug("RECV: {}".format(readbuf))
					ping_recv = True if "PING :tmi.twitch.tv" in readbuf else False
					if "PONG :" not in readbuf:
						self._socket_in_queue.insert(0, readbuf)	
				except socket.timeout:
					pass
			if ping_recv:
				with self._socket_out_lock:
					self._socket_out_queue.insert(0, 'PONG :tmi.twitch.tv')
				ping_recv = False
			time.sleep(.01)

	def _write_socket(self) -> None:
		''' Pop from the out queue and write it to the socket
		'''
		def read_soc():
			if len(self._socket_out_queue) == 0:
				return
			buf = self._socket_out_queue.pop() + '\r\n'
			#buf = "PRIVMSG #" + self._stream_to_watch + " :" + message + "\r\n"
			self._socket.send(buf.encode())
			logging.info("SENT: {}".format(buf))

		while True:
			with self._socket_out_lock:
				read_soc()
			time.sleep(.01)
			
	# ------------------- Public Methods ---------------------
	def send_msg(self,message) -> None:
		''' Use this method in your plugin to send messages into the chat
		'''
		# Sends 'message' to the socket using twitch API formatting
		buf = "PRIVMSG #" + self._stream_to_watch + " :" + message + "\r\n"
		with self._socket_out_lock:
			self._socket_out_queue.insert(0, buf)

	def get_user_and_message(self, buf) -> tuple:
		# Message is normal message
		if "PRIVMSG #{} :".format(self._stream_to_watch) not in buf:
			return None, None
		message = buf.split("#")
		received_user = buf.split("!")[0][1:].strip()
		received_message = buf.split("PRIVMSG #{} :".format(self._stream_to_watch))[1].strip();			
		return received_user, received_message

	def main_routine(self):
		''' While the bot is alive, keep reading messages and proessing them.
			After it dies, shutdown the socket and end. '''
		
		while(self._is_alive()):
			usr_msg = self.get_user_and_message()
			self._parse_command(usr_msg[0],usr_msg[1])
			
		t = threading.Thread( target = self._gui.destroy)
		t.daemon = True
		t.start()
		self._shutdown_socket()
		

import socket
import sys     
import time
from BotGUI import BotGUI
import threading
import os


class MyBot():
    def __init__(self, settings, plugins):
        ''' Initializes the socket and the Bot
        '''

        # Initialize GUI
        self._gui = BotGUI()

        # Setup object variables
        self._command_char = settings["command_char"]
        self._bytes_to_read = 1024
        self._port = 6667
        self._host = "irc.twitch.tv" 
        self._nick = settings["nick"]
        self._pass = settings["oauth"]
        self._stream_to_watch = settings["stream"]
        self._post_on_join = settings["post_on_join"]
        self._plugins = plugins

        # Start logging if it is set.
        self._logging = False
        if settings["logging"] == "1":
            self._start_logger()

        # Connect the socket
        self._socket = socket.socket()
        self._socket.settimeout(1)
        self.log("SYS: Created Socket")
    
        self._socket.connect((self._host,self._port))
        self.log("SYS: Connected socket to " + str(self._host) + ":" + str(self._port))

        self._send_initializers()
        

    # -------------- Private Methods ----------------

    def _start_logger(self):
        self._logging = True
        self._lock  = threading.Lock()
        now = time.strftime("%c")
        log_session = "================ LOG "
        log_session += str(now) + " " + self._stream_to_watch + " "
        log_session += "================"
        self._queue = [log_session]

        # Path of log.txt in the MyBot folder
        self._log_file_path = os.path.join(os.path.join(os.getcwd(),"MyBot"),"log.txt")        

        # Thread to write the queue to the file.
        t = threading.Thread( target = self._log_thread_to_file)
        t.daemon = True
        t.start()

        
    def _log_thread_to_file(self):
        ''' While the bot is alive,
            sleep for 5 seconds, then read all messages and add them to log.txt
        '''
        while(self._is_alive()):
            time.sleep(1)
            self._lock.acquire()
            fd = open(self._log_file_path,"a")
            for num in range(len(self._queue)):
                the_value = self._queue.pop(0)
                fd.write(the_value + "\n")
            fd.close()
            self._lock.release()


    def _add_to_log_queue(self, message):
        self._lock.acquire()
        self._queue.append(message)
        self._lock.release()
        
    def _send_initializers(self):
        ''' Sends initialization to the server '''
    
        PASS_S = "PASS " + self._pass + "\r\n"
        self._socket.send(PASS_S.encode())
    
        NICK_S = "NICK " + self._nick.lower() + "\r\n"
        self._socket.send(NICK_S.encode())

        JOIN_S = "JOIN #" + self._stream_to_watch + "\r\n"
        self._socket.send(JOIN_S.encode())
    
        self._read_beginning_intro()


    def _read_beginning_intro(self):
        ''' Reads the information that twitch api sends at 
              the beginning of the connection
        '''
        self.log("SYS: Initializing...")
        buf = self._socket.recv(self._bytes_to_read).decode()
        while "End of" not in buf:
            buf = self._socket.recv(self._bytes_to_read).decode()
        self.log("SYS: Ready.")
        self.log("SYS: Starting bot...")

        if self._post_on_join == "1":
            self.send_msg(self._nick + " has joined the channel. Type " + self._command_char + "commands for a list of commands.")
    


    def _check_ping(self, message):
        ''' Checks if the incoming message is a PING from the server.
             If it is, then send the corresponding message to the server.
        '''
        if message[:4] == "PING":
            self._socket.send("PONG tmi.twitch.tv\r\n".encode());


    def _shutdown_socket(self) -> None:
        ''' Unloads all memory from the program, shuts down the socket 
                and exits the program
        '''
        for plugin in self._plugins:
            plugin.unload_memory()
    
        self._socket.close()
        self.log("SYS: Shutdown successful")
        sys.exit()

    def _do_commands(self):
        ''' Does the simple 'commands' command in chat.
            Lists all commands from the bot.
            Uses each plugin __repr__ method
        '''
        message = self._command_char + "commands"
        for plugin in self._plugins:
            if str(plugin) != "None":
                message += ", " + self._command_char + str(plugin)
        self.send_msg(message)
        
    def _parse_command(self,username,message):
        ''' Parses each command from the chat
            If it triggers any plugins, then start those plugins
        '''
        if len(message) == 0:
            return
            
        if message[0] == self._command_char and message[1:] == "commands":
            self._do_commands()
            
        for plugin in self._plugins:
            if plugin.triggered(username,message, self._command_char):
                plugin.start(self)
                break;
            
    def _is_alive(self) -> bool:
        ''' Returns whether the gui SAFE EXIT button has been clicked
        '''
        return self._gui.is_alive()

    # ------------------- Public Methods ---------------------

    def send_msg(self,message) -> None:
        ''' Use this method in your plugin to send messages into the chat
        '''
        time.sleep(.5)
        # Sends 'message' to the socket using twitch API formatting
        buf = "PRIVMSG #" + self._stream_to_watch + " :" + message + "\r\n"
        self.log("Send: " + self._nick + ":" + message)
        self._socket.send(buf.encode())
        time.sleep(.5)


    def get_user_and_message(self) -> tuple:
        '''
         Use this function in your plugin to read from chat
         Read the username and message from the socket.
         Returns a tuple of the username / message
         If ping is sent, sends PONG to the socket
        '''
        
        try:
            readbuf = self._socket.recv(self._bytes_to_read).decode()
        except:
            return ("None","None")
        
        self._check_ping(readbuf)
        try:
            # Message is normal message
            message = readbuf.split("#")
            received_user = message[0].split("!")[0][1:].strip()
            received_message = message[1].split(":")[1].strip();            
            self.log("Recv: " + received_user + ": " + received_message)
            return (received_user,received_message)
        except:
            # Message is a ping from the server
            return ("PING","PONG")        
           
           
    def start_gui(self):
        ''' Starts the BotGUI for debugging and SAFE EXIT
        '''
        self._gui.main_routine()
        
        
    def log(self, msg):
        ''' Shows the message on the GUI
            Useful for debugging. 
            Can be used in plugins
        '''
        if (self._logging):
            self._add_to_log_queue(msg)
        self._gui.show(msg)
           
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
        
        

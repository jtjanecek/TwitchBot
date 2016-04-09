

import socket
import sys     
import time
from BotGUI import BotGUI
import threading


class MyBot():
    def __init__(self, plugins, command_character, nick, oauth, stream_to_watch, post_on_join):
        ''' Initializes the socket and the Bot
        '''
        self._command_char = command_character
        self._bytes_to_read = 1024
        self._port = 6667
        self._host = "irc.twitch.tv" 
        self._nick = nick
        self._pass = oauth
        self._stream_to_watch = stream_to_watch
        self._post_on_join = post_on_join
        self._plugins = plugins

        self._gui = BotGUI()

        self._socket = socket.socket()
        self.log(" Created Socket")
    
        self._socket.connect((self._host,self._port))
        self.log(" Connected socket to " + str(self._host) + ":" + str(self._port))

        self._send_initializers()
        

    # -------------- Private Methods ----------------
        
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
              the beginning
        '''
        self.log("Initializing...")
        buf = self._socket.recv(self._bytes_to_read).decode()
        while "End of" not in buf:
            buf = self._socket.recv(self._bytes_to_read).decode()
        self.log("Ready.")
        self.log("Starting bot...")

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
        self.log(" Shutdown successful")
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
        self.log(" ### Sending --> " + self._stream_to_watch + " :" + message)
        self._socket.send(buf.encode())
        time.sleep(.5)


    def get_user_and_message(self) -> tuple:
        '''
         Use this function in your plugin to read from chat
         Read the username and message from the socket.
         Returns a tuple of the username / message
         If ping is sent, sends PONG to the socket
        '''
        readbuf = self._socket.recv(self._bytes_to_read).decode()
        self._check_ping(readbuf)
        try:
            message = readbuf.split("#")
            received_user = message[0].split("!")[0][1:].strip()
            received_message = message[1].split(":")[1].strip();            
            self.log(received_user + " : " + received_message)
            return (received_user,received_message)
        except:
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
        
        
    

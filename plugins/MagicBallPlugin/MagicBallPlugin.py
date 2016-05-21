# 8 ball Plugin
import random
from datetime import datetime




class MagicBallPlugin():
    def __init__(self):
        ''' Initialize Plugin variables if needed
        '''
        self._list = ["It is certain.",
                      "It is decidedly so.",
                      "Without a doubt.",
                      "Yes, definitely.",
                      "You may rely on it.",
                      "As I see it, yes.",
                      "Most likely.",
                      "Outlook good."]
        self._size = len(self._list)
        
        
    # ==========================================================================
    #                      Methods Needed for every plugin    
    # ==========================================================================
    def name(self) -> str:
        return "MagicBallPlugin"
    
    def __str__(self) -> str:
        ''' Return the command used to start the plugin.
            Return "None" if it is a passive plugin (like this example) 
        '''
        return "ask"
        
    def start(self, mybot) -> None:
        ''' This method is called after the mybot knows that this plugin has been triggered
        '''
        random.seed(datetime.now())
        mybot.send_msg( self._list[int(random.random() * self._size) ] )
        
   
    def triggered(self, username, message, command_char) -> bool:
        ''' Returns whether this plugin is triggered by the username / message
        '''
        if len(message) < 4:
            return False;
        return message[0] == command_char and  message[1:4] == "ask"
    
    def unload_memory(self) -> None:
        ''' No need to unload memory in this example. 
            Only need to unload memory if the plugin uses memory from a file (like TriviaPlugin)
            This method is needed to save information when the bot shuts down
        '''
        return
        
        

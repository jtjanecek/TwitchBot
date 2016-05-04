# Roulette Plugin
import random
import time

class RoulettePlugin():
    def __init__(self):
        ''' Initialize Plugin variables if needed
        '''
        self._user_who_triggered = "empty"
        

    def _start_roulette(self, mybot):
        time.sleep(5)
        random.seed(time.time())
        gun_shot = int(random.random() * 6) + 1
        if gun_shot == 1:
            mybot.send_msg(" @#$%^&*( BOOM )(*&^%$#@    === YOU DIED === ")
        else:
            mybot.send_msg("Click.")

        
    # ==========================================================================
    #                      Methods Needed for every plugin    
    # ==========================================================================
    def name(self) -> str:
        return "RoulettePlugin"
    
    def __str__(self) -> str:
        ''' Return the command used to start the plugin.
            Return "None" if it is a passive plugin (like this example) 
        '''
        return "risk"
        
    def start(self, mybot) -> None:
        ''' This method is called after the mybot knows that this plugin has been triggered
        '''
        mybot.send_msg("Russian Roulette with " + self._user_who_triggered + "... Loading gun...")

        self._start_roulette(mybot)

   
    def triggered(self, username, message, command_char) -> bool:
        ''' Returns whether this plugin is triggered by the username / message
        '''
        if message[0] == command_char and message[1:] == "risk":
            self._user_who_triggered = username
            return True
        return False
    
    def unload_memory(self) -> None:
        ''' No need to unload memory in this example. 
            Only need to unload memory if the plugin uses memory from a file (like TriviaPlugin)
            This method is needed to save information when the bot shuts down
        '''
        return
        
        

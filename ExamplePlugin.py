# Example Plugin
'''
Simple example Plugin
See TriviaPlugin for a more complex plugin
'''



'''
This plugin will send Kappa if a user in the chat sends
a Kappa. This is a passive plugin
'''
class ExamplePlugin():
    def __init__(self):
        ''' Initialize Plugin variables if needed
        '''
        pass
        
        
    # ==========================================================================
    #                      Methods Needed for every plugin    
    # ==========================================================================
    
    def __str__(self) -> str:
        ''' Return the command used to start the plugin.
            Return "None" if it is a passive plugin (like this example) 
        '''
        return "None"
        
    def start(self, mybot) -> None:
        ''' This method is called after the mybot knows that this plugin has been triggered
        '''
        mybot.send_msg("Kappa")
   
    def triggered(self, username, message, command_char) -> bool:
        ''' Returns whether this plugin is triggered by the username / message
        '''
        return message == "Kappa"
    
    def unload_memory(self) -> None:
        ''' No need to unload memory in this example. 
            Only need to unload memory if the plugin uses memory from a file (like TriviaPlugin)
            This method is needed to save information when the bot shuts down
        '''
        return
        
        

# TwitchBot
A twitch bot made in python. 

# What You Need
1. A Twitch Account (for the bot to use)
2. An "oauth" password. Can be obtained here: https://twitchapps.com/tmi/
3. A Command Character: used before bot commands (example: "!commands", the command character is !)
4. A Stream You want your bot to join!

# Setup
config.txt contains all the default setup information. Change this to change the default settings.
You can run it without changing the defaults (and leave fields blank) and go to twitch.tv/examplebot1 to see the defaults of the bot.
After running main.py (with python 3.5 or higher) a gui will appear to let the user change the defaults at runtime.
The setup GUI can turned off by setting  "setup_gui=0" in config.txt.
After the bot joins the stream, another GUI will appear that will show logging information and an exit button.

# config.txt
* nick:         
	* The name of the bot (all lowercase)
* oauth: 
	* The authentication for the bot. Get yours at https://twitchapps.com/tmi/
* command_char: 
	* The command character. example: !commands (! is command character)
* stream:       
	* The stream for the bot to join
* setup_gui:    
	* Use SetupGUI for input of defaults; otherwise will use defaults in config.txt
* use_plugins:  
	* This will automatically enable or disable all plugins in the plugins folder
* post_on_join: 
	* The bot will post that it has joined the channel
* logging:      
	* Automatically log all chat in MyBot/log.txt

# Plugins
Plugin functionality for those users who know python. See ExamplePlugin and TriviaPlugin for examples.

# Creating Plugins
Follow the skeleton of ExamplePlugin.
Make a folder, .py module, and class with the same name (example ExamplePlugin).
Have the needed methods in your plugin class.
That't it.

# License
GPLv3

# TwitchBot
A twitch bot made in python. 

# What You Need
1. A Twitch Account (for the bot to use)
2. An "oauth" password. Can be obtained here: https://twitchapps.com/tmi/
3. A Command Character: used before bot commands (example: "!commands", the command character is !)
4. A Stream You want your bot to join!

You can either default these by using the config.txt, or you can manually enter them into the GUI.

# Setup
config.txt contains all the default setup information. Change this to change the default settings.
You can run it without changing the defaults (and leave fields blank) and go to twitch.tv/examplebot1 to see the defaults of the bot.
After running main.py (with python 3.5 or higher) a gui will appear to let the user change the defaults at runtime.
The setup GUI can turned off by setting  "setup_gui=0" in config.txt.
After the bot joins the stream, another GUI will appear that will show logging information and an exit button.

# config.txt
nick:         The name of the bot (twitch account you created). 
oauth:        The authentication for the bot. Get yours at https://twitchapps.com/tmi/ (Example: oauth:sjsdh135)
command_char: The command character. example: !commands (! is command character)
stream:       The stream for the bot to join.
setup_gui:    This will make the main GUI appear if you want to change defaults. (make this 0 if you know you want to go with the defaults)
post_on_join: The bot will post that it has joined the channel if this is 1.

# Plugins
Plugin functionality for those users who know python. See ExamplePlugin and TriviaPlugin for examples.

# Creating Plugins
Follow the skeleton of ExamplePlugin.
Make a folder, .py module, and class with the same name (example ExamplePlugin).
Have the needed methods in your plugin class.
That't it.

# License
GPLv3

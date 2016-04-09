# Author: John Janecek
# Created 3/19/2016

# ---------------------------------------------------------------------------------------
# The GUI for getting bot admin settings if you want to change the config.txt settings
# ---------------------------------------------------------------------------------------
from SettingsGUI import SettingsGUI

# ---------------------------------------------------------------------------------------
# Main bot code
# ---------------------------------------------------------------------------------------
from MyBot import MyBot

# ---------------------------------------------------------------------------------------
# Plugins... Also have to append to the plugins list in the main() function
# Each plugin must have functioned defined in the README
# ---------------------------------------------------------------------------------------
from plugins import initialize_plugins

# Used for running the main routine at the same time as the GUI
import threading




def read_config() -> dict:
    # Returns a dictionary with all the settings from config.txt
    settings = dict()
    f = open("config.txt","r")
    lines = f.read().splitlines()
    f.close()
    for line in lines:
        temp = line.split("=")
        settings[temp[0]] = temp[1]
    return settings


def main():
    settings = read_config()
    plugins = initialize_plugins()
    
    settings = SettingsGUI(settings).main_routine()

    # Run Main Routine to start the bot
    mybot = MyBot(plugins, settings["command_char"], settings["nick"], settings["oauth"], settings["stream"])
    t = threading.Thread(target = mybot.main_routine)
    t.daemon = True
    t.start()
    mybot.start_gui()

if __name__ == "__main__":
    main()

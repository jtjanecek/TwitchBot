# Author: John Janecek
# Created 3/19/2016


# ---------------------------------------------------------------------------------------
# Plugins... Also have to append to the plugins list in the main() function
# Each plugin must have functioned defined in the README
# ---------------------------------------------------------------------------------------

# Used for running the main routine at the same time as the GUI
import threading


import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"plugins"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"guis"))


from SettingsGUI import SettingsGUI
from plugins import initialize_plugins
from MyBot import MyBot



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

def start_bot(settings,plugins):
    mybot = MyBot(plugins, settings["command_char"], settings["nick"], settings["oauth"], settings["stream"], settings["post_on_join"])
    t = threading.Thread(target = mybot.main_routine)
    t.daemon = True
    t.start()
    mybot.start_gui()


def main():
    settings = read_config()

    if settings["use_plugins"] == "1":
        plugins = initialize_plugins()
    else:
        plugins = []

    if settings["setup_gui"] == "1":
        settings = SettingsGUI(settings,plugins).main_routine()

    # Run Main Routine to start the bot
    
    start_bot(settings,plugins)
    

if __name__ == "__main__":
    main()

import threading
import signal
import logging

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"plugins"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"TwitchChatBot"))
os.environ['PYTHONUNBUFFERED'] = 'True'

from plugins import initialize_plugins
from TwitchChatBot import TwitchChatBot

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

'''
def start_bot(settings,plugins):

    # Start the bot
    mybot = MyBot(settings,plugins)
    t = threading.Thread(target = mybot.main_routine)
    t.daemon = True
    t.start()
'''

def signal_handler(sig, frame):
	logging.info("Sig: {}".format(sig))
	logging.info("Frame: {}".format(frame))
	logging.info("End signal detected...")
	logging.info('Done!')
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Settings based on config.txt
settings = read_config()

if settings['cli'] == 'disable':
	logging.basicConfig(level=logging.DEBUG,
              format='%(asctime)s - %(module)s - %(levelname)s - %(message)s',
              datefmt='%m-%d-%y %H:%M',
              filename='logs/log.log',
              filemode='w')
else: # Output to CLI
	logging.basicConfig(level=logging.DEBUG,
              format='%(asctime)s - %(module)s - %(levelname)s - %(message)s',
              datefmt='%m-%d-%y %H:%M')

logging.info("Using PID: {}".format(os.getpid()))

# Initialize Plugins
#   initialize_plugins() comes from plugins.py in the plugins folder
if settings["use_plugins"] == "1":
	plugins = initialize_plugins()
else:
	plugins = []

# Run Main Routine to start the bot
TwitchChatBot(settings,plugins)

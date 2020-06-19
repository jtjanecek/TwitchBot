import sys
import os
id = sys.argv[1]
with open("logs/log.log", 'r') as log:
	pid_to_kill = next(log).split("PID: ")[1]

os.system("kill -2 {}".format(pid_to_kill))

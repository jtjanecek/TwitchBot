import sys
import time
def follow(thefile):
	thefile.seek(0,2)
	while True:
		line = thefile.readline()
		if not line:
			time.sleep(0.1)
			continue
		yield line

def toPrint(line):
	return "INFO" in line or "ERROR" in line

if __name__ == '__main__':
	id = sys.argv[1]
	with open('logs/{}.log'.format(id),'r') as logfile:
		for line in logfile:
			if toPrint(line):
				print(line.strip())

	with open('logs/{}.log'.format(id),'r') as logfile:
		loglines = follow(logfile)
		for line in loglines:
			if toPrint(line):
				print(line.strip())

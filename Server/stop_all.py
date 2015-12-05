import os, signal

OUTPUT_PROCESS_IDS = ".pids"

try:
	pidsFile = open(OUTPUT_PROCESS_IDS, "r")
	pids = pidsFile.read();
	pidsFile.close()

	pids = pids.split('\n')

	count = 0

	pidsFile = open(OUTPUT_PROCESS_IDS, "w")

	for pid in pids:
		if pid.isdigit():
			try:
				print "Killing process", pid
				os.kill(int(pid), signal.SIGTERM)
				count += 1
			except:
				print "Can't kill process", pid
				pidsFile.write(pid + "\n")

	pidsFile.close()

	print count, "process killed"
except:
	print "Can't open .pids file. You are root?"
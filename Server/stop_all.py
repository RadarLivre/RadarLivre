import os, signal

OUTPUT_PROCESS_IDS = ".pids"

pidsFile = open(OUTPUT_PROCESS_IDS, "r")
pids = pidsFile.read();
pidsFile.close()

pids = pids.split('\n')

count = 0
for pid in pids:
	if pid.isdigit():
		try:
			print "Killing process", pid
			os.kill(int(pid), signal.SIGTERM)
			count += 1
		except:
			print "Can't kill process", pid

pidsFile = open(OUTPUT_PROCESS_IDS, "w")
pidsFile.close()

print count, "process killed"
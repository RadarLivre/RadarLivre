import subprocess
import inspect, os

OUTPUT_PROCESS_IDS = ".pids"
CURRENT_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

pids = []

process = subprocess.Popen(["nohup", "python", os.path.join(CURRENT_PATH, "ServerCollect/start_server_collect.py")])
pids.append(process)
print "Start ServerCollect with id", process.pid

process = subprocess.Popen(["nohup", "python", os.path.join(CURRENT_PATH, "ServerCollect/start_collector.py")])
pids.append(process)
print "Start Collector with id", process.pid

process = subprocess.Popen(["nohup", "python", os.path.join(CURRENT_PATH, "DatabaseServer/start_database_server.py")])
pids.append(process)
print "Start DatabaseServer with id", process.pid

pidsFile = open(OUTPUT_PROCESS_IDS, "a")
s = ""

for p in pids:
	s += str(p.pid) + "\n"

pidsFile.write(s)

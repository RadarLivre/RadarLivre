import multiprocessing

cores = multiparallelism = multiprocessing.cpu_count()
workers = max(2, cores * 2 + 1)
threads = 4 

bind = "0.0.0.0:8000"
worker_class = "gthread" 
timeout = 30 
keepalive = 5  
max_requests = 1000  
max_requests_jitter = 50  

accesslog = "-" 
errorlog = "-"   
loglevel = "info"

preload_app = True  
reuse_port = True   
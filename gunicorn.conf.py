"""
Configuring gunicorn.

Override any settings in api_lib.gunicorn by adding them directly
in this file.

For options see:
http://docs.gunicorn.org/en/stable/configure.html#configuration-file
"""
import multiprocessing

preload_app = False
bind = "0.0.0.0:8000"

timeout = 300
loglevel = "info"

workers = multiprocessing.cpu_count()
# worker_tmp_dir = "/dev/shm"

worker_class = "uvicorn.workers.UvicornWorker"

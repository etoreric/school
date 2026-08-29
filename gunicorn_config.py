import os
import multiprocessing

# Server Socket
bind = os.environ.get("GUNICORN_BIND", f"0.0.0.0:{os.environ.get('PORT', '8080')}")
backlog = 2048

# Worker Processes
workers = int(os.environ.get("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1))
worker_class = os.environ.get("GUNICORN_WORKER_CLASS", "gthread")
threads = int(os.environ.get("GUNICORN_THREADS", "2"))
worker_connections = 1000
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "120"))
keepalive = int(os.environ.get("GUNICORN_KEEPALIVE", "5"))

# Server Mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = os.environ.get("GUNICORN_ACCESS_LOG", "-")
errorlog = os.environ.get("GUNICORN_ERROR_LOG", "-")
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s µs'

# Process Naming
proc_name = "sunny_school_cms"

# Lifecycle Hooks
def on_starting(server):
    server.log.info("Starting Sunny High School CMS Gunicorn Server...")

def on_reload(server):
    server.log.info("Reloading Sunny High School CMS Gunicorn Server...")

def when_ready(server):
    server.log.info("Sunny High School CMS is ready to handle requests.")

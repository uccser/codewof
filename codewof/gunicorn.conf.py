"""Configuration file for gunicorn."""

from multiprocessing import cpu_count

# Worker count from http://docs.gunicorn.org/en/stable/design.html#how-many-workers
workers = cpu_count() * 2 + 1
# Details from https://cloud.google.com/appengine/docs/flexible/python/runtime
worker_class = "gevent"
forwarded_allow_ips = "*"
secure_scheme_headers = {"X-APPENGINE-HTTPS": "on"}

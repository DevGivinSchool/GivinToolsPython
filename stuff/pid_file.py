#https://docs.python.org/3/library/atexit.html


import os
import sys

pid = str(os.getpid())
pidfile = "/tmp/mydaemon.pid"

if os.path.isfile(pidfile):
    print(f"{pidfile} already exists, exiting")
    sys.exit()
    file(pidfile, 'w').write(pid)
try:
    pass
finally:
    os.unlink(pidfile)

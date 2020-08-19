import os

path = "c:\MyGit\GivinToolsPython\sf\sf_main.py"
t1 = os.path.dirname(os.path.dirname(path))
print(t1)
t2 = os.path.relpath(t1, start=os.curdir)
print(t2)
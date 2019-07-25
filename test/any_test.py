import os
import sys
from pprint import pprint

if 'ymail_login' in os.environ:
    ymail_login = os.environ.get('ymail_login')
else:
    print("I can't see env ymail_login")
    pprint(os.environ)
    sys.exit(1)

if 'ymail_password' in os.environ:
    ymail_login = os.environ.get('ymail_password')
else:
    print("I can't see env ymail_password")
    sys.exit(1)

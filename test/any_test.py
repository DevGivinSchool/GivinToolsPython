import os
import sys

#print(os.environ)

if 'ymail_login' in os.environ:
    ymail_login = os.environ.get('ymail_login')
    print(ymail_login)
else:
    print("I can't see env ymail_login")
    sys.exit(1)

if 'ymail_password' in os.environ:
    ymail_password = os.environ.get('ymail_password')
    print(ymail_password)
else:
    print("I can't see env ymail_password")
    sys.exit(1)

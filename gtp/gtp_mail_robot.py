from imapclient import IMAPClient
from PASSWORDS import *
import email

# context manager ensures the session is cleaned up
with IMAPClient(host="imap.yandex.ru", use_uid=True) as client:
    a = client.login(ymail_login, ymail_password)
    #print(a)

    b = client.select_folder('INBOX')
    print(b)

    # search criteria are passed in a straightforward way
    # (nesting is supported)
    messages = client.search(['ALL'])
    print(messages)

    # fetch selectors are passed as a simple list of strings.
    response = client.fetch(messages, ['RFC822'])
    print(response)
    print(response.items())

    # `response` is keyed by message id and contains parsed,
    # converted response items.
    for uid, message_data in client.fetch(messages, 'RFC822').items():
        email_message = email.message_from_bytes(message_data[b'RFC822'])
        print(uid, email_message.get('From'), email_message.get('Subject'))

    #print(client.capabilities())
    #print(client.list_folders())
    #print(client.noop())
    #print(client.welcome)

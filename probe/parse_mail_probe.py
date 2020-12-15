import email
# import unicodedata

f = open("mail.txt", "r")
email_message = f.read()
f.close()
# print(email_message)
# ffrom = email_message.get('From')
# fsubject =  email_message.get('Subject')
# print(f"ffrom={ffrom}")
# print(f"fsubject={fsubject}")
# print(email.message_from_string(email_message))


def get_decoded_email_body(message_body):
    """ Decode email body.
    Detect character set if the header is not set.
    We try to get text/plain, but if there is not one then fallback to text/html.
    :param message_body: Raw 7-bit message body input e.g. from imaplib. Double encoded in quoted-printable and latin-1
    :return: Message body as unicode string
    """

    msg = email.message_from_string(message_body)
    # msg = message_body

    text = ""
    if msg.is_multipart():
        html = None
        for part in msg.get_payload():

            print("%s, %s" % (part.get_content_type(), part.get_content_charset()))

            if part.get_content_charset() is None:
                # We cannot know the character set, so return decoded "something"
                text = part.get_payload(decode=True)
                continue

            charset = part.get_content_charset()

            if part.get_content_type() == 'text/plain':
                text = part.get_payload(decode=True).decode(str(charset), "ignore").encode('utf8', 'replace')
                text = part.get_payload(decode=True).decode(str(charset), "ignore")

            if part.get_content_type() == 'text/html':
                html = part.get_payload(decode=True).decode(str(charset), "ignore").encode('utf8', 'replace')
                html = part.get_payload(decode=True).decode(str(charset), "ignore")

        if text is not None:
            return text.strip()
        else:
            return html.strip()
    else:
        text = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
        text = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore')
        return text.strip()


print(get_decoded_email_body(email_message))

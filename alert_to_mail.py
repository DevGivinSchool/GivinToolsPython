import smtplib, ssl
import PASSWORDS


def send_mail(receiver_email, message, sender_email="robot@givinschool.org", port=465):
    # Create a secure SSL context
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.yandex.ru", port, context=context)
    server.login(PASSWORDS.logins['ymail_login'], PASSWORDS.logins['ymail_password'])
    server.sendmail(sender_email, receiver_email, message)


if __name__ == "__main__":
    mail_to = PASSWORDS.logins['admin_emails']
    msg = """\
    Subject: Hi there

    This message is sent from Python."""
    send_mail(mail_to, msg)

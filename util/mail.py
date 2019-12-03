import smtplib
from email.message import EmailMessage


class Mail:
    def __init__(self):
        pass

    def sendMail(self, menssagem, destinatario):
        gmail_user = 'trabalhoredes2019@gmail.com'
        gmail_password = 'trabalhoredes'
        msg = EmailMessage()
        msg.set_content(menssagem)
        msg['From'] = gmail_user
        msg['To'] = destinatario
        msg['Subject'] = "Modificações no arquivo"
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, destinatario, msg.as_string())
            server.close()
            print("Email enviado")
        except:
            print('Deu ruim no envio do e-mail')

import smtplib

class Mail:
    def senMail(self, menssagem, destinatario):
        gmail_user = 'trabalhoredes2019@gmail.com'
        gmail_password = 'trabalhoredes'
        Subject: "Modificações no arquivo"
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, destinatario, menssagem)
            server.close()
            print("deu certo o envio do email")
        except:
            print('Deu ruim no envio do e-mail')
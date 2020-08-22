import email, smtplib, ssl
import time

from email import encoders
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio



def send_audio_data(config):
    subject = config['subject']
    body = f'Recorded at {time.strftime("%H:%M:%S", time.localtime())}'
    sender = config['sender']
    receiver = config['receiver']
    password = config['password']


    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message["Bcc"] = receiver

    message.attach(MIMEText(body, "plain"))


    filename = "temp.wav"

    with open(filename, "rb") as audio:
        part = MIMEAudio(audio.read(), _subtype="wav")

    part.add_header("Content-Disposition", "attachement", filename=filename)

    message.attach(part)
    text = message.as_string()


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        
        try:
            server.login(sender, password)

        except smtplib.SMTPAuthenticationError as e:
            print(e)
            print('''
            Probably the gmail spam security is blocking you, because it considered the Script as an untrusted source.
            There are some options to remove the error:
            1) Allow less secure Apps to use your account: https://myaccount.google.com/lesssecureapps. 
            (>ou can create a ThrowAway-Account for this, instead of using your personal account)
            2) Use other email provider like outlook, with fewer security standards
            ''')
            raise KeyboardInterrupt

        server.sendmail(sender, receiver, text)
        print('send email')
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

def send_email(email_receiver, name_receiver):
    try:
        load_dotenv()

        email_sender = os.getenv("ACCOUNT")
        password = os.getenv("ACCOUNT_PASSWORD")

        subject = f"¡Hola {name_receiver}!"
        body = f"""
        Hola {name_receiver} ¡El sistema de detección de talleristas de Apprende te ha encontrado! se te envía este correo con la intención de que nos puedas compartir una propuesta de un taller y así podamos trabajar juntos.
        Lo cual podrás realizar mediante el siguiente link de formulario de contacto: https://forms.gle/2LWtV9Xaix3nhvJ98
        """

        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["Subject"] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com",465,context= context) as smtp:
            smtp.login(email_sender,password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        return 1
    except:
        return 0
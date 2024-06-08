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
        Hola {name_receiver},

        Nos complace informarte que has sido seleccionado por nuestro sistema de detección de talleristas de Apprende como un candidato ideal para colaborar con nosotros. Estamos entusiasmados por la posibilidad de trabajar contigo y estamos interesados en conocer más sobre tus propuestas de talleres.
        Para avanzar en esta colaboración, te invitamos a compartir una propuesta de taller con nosotros. Puedes hacerlo a través del siguiente formulario de contacto:

        [Formulario de Propuesta de Taller] (https://forms.gle/2LWtV9Xaix3nhvJ98)

        Agradecemos de antemano tu tiempo y esperamos con interés recibir tu propuesta. Si tienes alguna pregunta o necesitas más información, no dudes en contactarnos.

        Saludos cordiales,
        Equipo de Apprende
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
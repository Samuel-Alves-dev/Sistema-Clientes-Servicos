import smtplib
from email.message import EmailMessage
import mimetypes
from datetime import datetime
import relatorio_pdf as relpdf
import os


email_assunto = "Relatório geral dos Clientes e seus Serviços"
data = datetime.now().strftime("%d/%m/%Y")
email_mensagem = f"""Olá Chefe!
Aqui está o relatório geral do dia {data}.
"""

def enviar_email():
    con = relpdf.conectar_banco()
    cursor = con.cursor()
    cursor.execute("SELECT remetente, destinatario, app_password FROM emails_registrados LIMIT 1")
    infsg = cursor.fetchall()
    cursor.close()
    infs = infsg[0]
    email_remetente = infs[0]
    email_destinatario = infs[1]
    email_senha = f"{infs[2][:4]} {infs[2][4:8]} {infs[2][8:12]} {infs[2][12:]}"
    email_anexo = relpdf.caminho_pdf_gerado
    msg = EmailMessage()
    msg["From"] = email_remetente
    msg["To"] = email_destinatario
    msg["Subject"] = email_assunto
    msg.set_content(email_mensagem)

    mime_type, _ = mimetypes.guess_type(email_anexo)
    mime_type, mime_subtype = mime_type.split("/")

    with open(email_anexo, "rb") as arquivo:
        msg.add_attachment(arquivo.read(),maintype="application",subtype="pdf",filename=os.path.basename(email_anexo))

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as email:
        email.login(email_remetente,email_senha)
        email.send_message(msg)
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(subject, body):
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")

    message = Mail(
        from_email=sender_email,
        to_emails=receiver_email,
        subject=subject,
        html_content=body)

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print("Correo electrónico enviado correctamente.")
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("Error al enviar el correo electrónico:", e)

if __name__ == "__main__":
    subject = "Alerta de Temperatura"
    body = "La temperatura por debajo de 20°C."
    send_email(subject, body)
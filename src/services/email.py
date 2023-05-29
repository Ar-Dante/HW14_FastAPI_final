import logging
from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.conf.config import settings
from src.services.auth import auth_service

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=EmailStr(settings.mail_from),
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Cat System Corporation",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    The send_email function sends an email to the user with a link to confirm their email address.
        The function takes in three parameters:
            -email: the user's email address, which is used as a recipient for the message and also as part of
                the token verification payload. This parameter must be of type EmailStr (a custom class that validates
                whether or not an input string is a valid email). If it isn't, then this function will raise an exception.

    :param email: EmailStr: Ensure that the email is a valid email address
    :param username: str: Get the username of the user who is trying to register
    :param host: str: Send the host to the email template
    :return: A coroutine object, which is an awaitable
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email!",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        logging.error(err)

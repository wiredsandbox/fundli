import requests

from fundli.errors.error import Error
from fundli.settings.settings import (
    DOMAIN_NAME,
    EMAIL_FILE_PATH,
    MAIL_API_KEY,
    MAIL_URL,
)

from .email_schema import EmailResponse, EmailSchema


def render_template(template_name: str, context: dict):
    # load the template
    template = EMAIL_FILE_PATH.get_template(template_name)

    # render the template
    return template.render(context)


def send_email(body: EmailSchema):
    res = requests.post(
        f"{MAIL_URL}",
        data={
            "from": body.sender_email,
            "fromName": body.sender_name,
            "to": body.recipients,
            "subject": body.subject,
            "bodyHtml": render_template(
                body.email_template.value,
                {
                    "verification_code": body.body,
                    "username": body.first_name,
                    "logo_url": DOMAIN_NAME + "/files/logo",
                },
            ),
            "bodyText": body.body,
            "isTransactional": True,
            "apiKey": MAIL_API_KEY,
        },
    )
    return is_email_successful(res)


def is_email_successful(res):
    if res.status_code == 200:
        return EmailResponse(message="email sent successfully")
    return Error("failed to send email", 500)

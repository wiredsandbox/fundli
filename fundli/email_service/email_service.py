import requests

from fundli.errors.error import Error
from fundli.settings.settings import (
    DOMAIN_NAME,
    EMAIL_FILE_PATH,
    MAIL_API_KEY,
    MAIL_URL,
)

from .email_schema import EmailResponse, EmailSchema

# fucntion to send email based on the template
# def send_email(body: EmailSchema):
#     return requests.post(
#         f"{MAIL_URL}",
#         auth=("api", f"{MAIL_API_KEY}"),
#         data={
#             "from": f"{body.sender_name}" f" <{body.sender_email}>",
#             "subject": f"{body.subject}",
#             "to": body.recipients,
#             "html": render_template(
#                 body.email_template.value,
#                 {
#                     "verification_code": body.body,
#                     "username": body.first_name,
#                     "logo_url": DOMAIN_NAME + "/files/logo",
#                 },
#             ),
#         },
#     )


def send_message(body: str, sender_name: str, sender_email: str, recipients: list):
    # send email
    return requests.post(
        f"{MAIL_URL}",
        auth=("api", f"{MAIL_API_KEY}"),
        data={
            "from": f"{sender_name}" f" <{sender_email}>",
            "to": recipients,
            # check if body is a string or a html template
            "html" if "<" in body else "text": body,
        },
    )


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
    return False, Error("failed to send email", 500)

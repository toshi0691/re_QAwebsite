import sendgrid
from sendgrid.helpers.mail import *

SENDGRID_API    = "ここにAPIKeyを記述する"

sg          = sendgrid.SendGridAPIClient(api_key=SENDGRID_API)
from_email  = Email("送信元のメールアドレス")
to_email    = To("宛先のメールアドレス")
subject     = "メールの件名"
content     = Content("text/plain", "ここに本文")
mail        = Mail(from_email, to_email, subject, content)
response    = sg.client.mail.send.post(request_body=mail.get())
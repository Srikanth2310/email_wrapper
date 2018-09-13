import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey='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')
from_email = Email("potipireddisrikanth@gmail.com")
to_email = Email("potipireddi.srikanth@gmail.com")
subject = "Sending with SendGrid is Fun"
content = Content("text/plain", "and easy to do anywhere, even with Python")
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)

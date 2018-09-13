import sendgrid
import boto3
import os
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm #use the native Django form
from django.contrib.auth import login, logout
from django.template.loader import get_template
from django.conf import settings

from sendgrid.helpers.mail import *
from botocore.exceptions import ClientError

# Create your views here.

def login_view(request):
    return render(request,"login.html",{})

def after_login_view(request):
    return render(request,"after_login.html",{})


sg = sendgrid.SendGridAPIClient(apikey='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')
CONFIGURATION_SET = "ConfigSet"
BODY_HTML = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
            """
SENDER = "Srikanth <potipireddi.srikanth@gmail.com>"
AWS_REGION = "us-west-2"
CHARSET = "UTF-8"
client = boto3.client('ses',region_name=AWS_REGION)

def mail_deliver_view(request):
    #api_key_id = "potipi"
    #response = sg.client.api_keys._(api_key_id).get()
    #print response.status_code
    #print response.body
    #print response.header
    #sg = sendgrid.SendGridAPIClient(apikey='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')
    #sg_response = sg.client.suppression.bounces.get()
    #print("send grid response is: " + str(sg_response.status_code))
    #if sg_response.status_code == 200:
    #    print("we are good to go with snedGrid")
    #print(sg_response.body)
    #print(sg_response.headers)
    if request.method == "POST":
        print("calling mail delvier view")
        name = request.POST.get("name")
        to_email = request.POST.get("email")
        message = request.POST.get("message")
        subject = request.POST.get("subject")

        from_email = settings.DEFAULT_FROM_EMAIL
        email_to = [to_email]

        #First method
        #mail_message = "{0}, from {1} with email {2}".format(message,name,email_to)

        #second method
        context = {
            'user':name,
            'email':email_to,
            'message':message
        }
        mail_message = get_template('mail_message.txt').render(context)
        #send_mail(subject,mail_message,from_email,email_to,fail_silently=False)

        #use sendgrid api

        data = {
          "personalizations": [
            {
              "to": [
                {
                  "email": to_email
                }
              ],
              "subject": subject
            }
          ],
          "from": {
            "email": "potipireddisrikanth@gmail.com"
          },
          "content": [
            {
              "type": "text/plain",
              "value": message
            }
          ]
        }
        #mail = Mail(Email("poipireddisrikanth@gmail.com"), subject, email2, Content("text/plain",message))
        #print(mail.get())
        response = sg.client.mail.send.post(request_body=data)
        print(response.status_code)
        print(response.body)
        print(response.headers)

        if(response.status_code != 200):
            try:
                #Provide the contents of the email.
                response = client.send_email(
                    Destination={
                        'ToAddresses': [
                            to_email,
                        ],
                    },
                    Message={
                        'Body': {
                            'Html': {
                                'Charset': CHARSET,
                                'Data': BODY_HTML,
                            },
                            'Text': {
                                'Charset': CHARSET,
                                'Data': message,
                            },
                        },
                        'Subject': {
                            'Charset': CHARSET,
                            'Data': subject,
                        },
                    },
                    Source=SENDER,
                    # If you are not using a configuration set, comment or delete the
                    # following line
                    #ConfigurationSetName=CONFIGURATION_SET,
                )
            # Display an error if something goes wrong.
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                print("Email sent! Message ID:"),
                print(response['MessageId'])

    return render(request,"after_login.html",{})


#def ses_deliver_view(request):
#    if request.method == "POST":
#        name = request.POST.get("name")
#        to_email = request.POST.get("email")
#        message = request.POST.get("message")
#        subject = request.POST.get("subject")




    #return render(request,"after_login.html",{})

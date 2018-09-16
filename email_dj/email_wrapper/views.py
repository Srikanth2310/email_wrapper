import sendgrid
import boto3
import os
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm #use the native Django form
from django.contrib.auth import login, logout, authenticate
from django.views.generic import View
from django.template.loader import get_template
from django.conf import settings

from sendgrid.helpers.mail import *
from botocore.exceptions import ClientError

from .forms import UserForm

# Create your views here.

def login_view(request):
    return render(request,"login.html",{})

def after_login_view(request):
    return render(request,"after_login.html",{})

#prepare the data
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
#sg = sendgrid.SendGridAPIClient(apikey='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') #send grid obkect
#params = {'start_time': 1, 'end_time': 1}
#response = sg.client.suppression.bounces.get(query_params=params)
#print("send grid response is: " + str(bounce_response.status_code))

#api_key_id = "srikanth_icici"
#key_response = sg.client.api_keys._(api_key_id).get()

CONFIGURATION_SET = "ConfigSet"
BODY_HTML = """<html>
<head></head>
<body>
  <p>Django is fun</p>
</body>
</html>
            """
SENDER = "Srikanth <potipireddi.srikanth@gmail.com>"
AWS_REGION = "us-west-2"
CHARSET = "UTF-8"
client = boto3.client('ses',region_name=AWS_REGION) #SES object
count_of_mails = 0

def mail_deliver_view(request):
    count_of_mails = 0
    print(os.environ.get('SENDGRID_API_KEY'))
    #print("send grid response is: " + str(response.status_code))

    if request.method == "POST":
        count_of_mails += 1
        print("calling mail delvier view")
        print("mails attmepted to send:" + str(count_of_mails))
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

        #if failed from sendgrid
        if(response.status_code != 202):
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
                )
            
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                print("Email sent! Message ID:"),
                print(response['MessageId'])

    return render(request,"after_login.html",{'count_of_mails':count_of_mails})




#Handle User Registrations.
class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'
    #template_name = 'login.html'

    #balnk form
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        #print(form.is_valid())
        #print(form.errors)
        if form.is_valid():

            user = form.save(commit=False)
            #cleaned data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            #return user object
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect(mail_deliver_view)

        return render(request,self.template_name,{'form':form})


#Handle login
class UserLoginView(View):
    form_class = UserForm
    template_name = 'login.html'

    #balnk form
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect(mail_deliver_view)

        return render(request,self.template_name,{'form':form})

#Handle Logout
class UserLogoutView(View):
    
    template_name = 'login.html'
    def get(self, request):
        logout(request)
        return render(request,self.template_name,{})

This README is an intention to explain the project to the evaluator

Frameworks used --> Django
Advantages:
- Full Stack framework
- Inbuilt user authentication system

For the CSS templates --> Free bootstrap templates

The project (Email Service Project):
Local Host : http://127.0.0.1:8000 (default local server)
Setting up a local project would require many dependancy installations.
I working on setting up Amazon EC2 server


Backend Implementation:
Registration, Logging & Logout Systems --> Class based Views
APIS used for sending mails --> SendGrid(default) & Amazon SES

Areas to look for the code:
- email_dj/urls.py
- email_wrapper/views.py
- templates/*


Django Admin --> potipi/*******2310:
- Use this and check if users have been added properly to the database after registration

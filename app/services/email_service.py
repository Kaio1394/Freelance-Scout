from app.helpers.email_helper import EmailHelper
import os

class EmailService:
    def __init__(self, email_helper: EmailHelper):
        self.email_helper = email_helper
        
    def define_credentials(self):
        self.email_helper.set_credentials(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
        
    def define_configs_email(self, subject: str, body: str):
        self.email_helper.set_subject(subject)
        self.email_helper.set_email_to(os.getenv("EMAIL_TO"))
        self.email_helper.set_type_server_email(os.getenv("EMAIL_SERVER"))
        self.email_helper.set_body(body)
        
    def send(self):
        self.email_helper.send()
        
    def connect(self):
        return self.email_helper.connect()
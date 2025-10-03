import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.helpers.exceptions import EmailConnectionError, EmailSendError
from app.schemas.freelancer_schema import FreelancerBase

STATUS_CONNECTION_ACTIVE = 205

class EmailHelper:
    def __init__(self):
        self.__email = None
        self.__password = None  
        self.__smpt_server = None
        self.__smtp_port = None  
        self.__email_to: str = None
        self.__subject: str = None
        self.__message = None
        self.__body_html = None
        self.__server = None
    
    def _get_server_email(self, type_server: str) -> tuple[str, int]:
        match type_server.lower():
            case "gmail":
                return "smtp.gmail.com", 587
            case "hotmail":
                return "smtp.office365.com", 587    
            case "zoho":
                return "smtp.zoho.com", 587
            case "outlook":
                return "smtp.office365.com", 587 
            case _:
                raise ValueError(f"Type of email server [{type_server}] invalid.") 
    
    def connect(self) -> tuple[bool, str]:
        try:
            self.__server = smtplib.SMTP(self.__smpt_server, self.__smtp_port)
            self.__server.starttls()
            self.__server.login(self.__email, self.__password)
            return True, ""
        except Exception as err:
            return False, str(err)

    def disconnect(self):
        try:
            if self.__server is not None:               
                status = self.__server.noop()[0]
                if status == STATUS_CONNECTION_ACTIVE:
                    self.__server.quit()
        except smtplib.SMTPServerDisconnected:
            pass
        except Exception as e:
            raise RuntimeError("Erro ao desconectar do servidor SMTP") from e
        finally:
            self.__server = None
            
    def send(self):
        try:
            if self.__server is None:
                raise EmailConnectionError()              
            self.__message = MIMEMultipart()
            self.__message["From"] = self.__email
            self.__message["To"] = self.__email_to
            self.__message["Subject"] = self.__subject
            # self.__message.attach(MIMEText(self.__body, "plain"))
            self.__message.attach(MIMEText(self.__body_html, "html"))
            self.__server.sendmail(self.__email, self.__email_to, self.__message.as_string())
        except Exception as e:
            raise EmailSendError(str(e))
        
    def set_type_server_email(self, type_server: str):
        self.__smpt_server, self.__smtp_port = self._get_server_email(type_server)
        
    def set_credentials(self, email: str, password: str):
        self.__email = email
        self.__password = password
        
    def set_email_to(self, email_to: str):
        self.__email_to = email_to
        
    def set_subject(self, subject: str):
        self.__subject = subject
               
    def set_body_html(self, html: str):
        self.__body_html = html
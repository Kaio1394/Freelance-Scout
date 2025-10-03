from app.helpers.email_helper import EmailHelper
import os
from app.schemas.freelancer_schema import FreelancerBase

class EmailService:
    def __init__(self, email_helper: EmailHelper):
        self.email_helper = email_helper
        
    def define_credentials(self):
        self.email_helper.set_credentials(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
        
    def define_configs_email(self):
        self.email_helper.set_subject(os.getenv("EMAIL_SUBJECT"))
        self.email_helper.set_email_to(os.getenv("EMAIL_TO"))
        self.email_helper.set_type_server_email(os.getenv("EMAIL_SERVER"))
        
    def send(self, html: str):
        self.email_helper.set_body_html(html)
        self.email_helper.send()
        
    def connect(self):
        return self.email_helper.connect()
    
    def generate_html(self, list_freela: list[FreelancerBase]) -> str:
        html = """<html><head><meta charset="utf-8"><style>
        body{font-family:Arial,sans-serif;background:#f9f9f9;padding:20px;}
        .job{background:white;border-radius:8px;padding:15px;margin-bottom:15px;box-shadow:0 2px 4px rgba(0,0,0,0.1);}
        .job h2{margin-top:0;color:#333;}
        .job p{margin:5px 0;}
        .skills span{background:#eee;border-radius:4px;padding:2px 6px;margin-right:5px;font-size:0.9em;}
        a{color:#1a73e8;text-decoration:none;}
        </style></head><body>"""

        for job in list_freela:
            skills_html = " ".join([f"<span>{s}</span>" for s in job.skills]) if job.skills else "<i>Sem skills</i>"
            html += f"<div class='job'><h2><a href='{job.link}'>{job.title}</a></h2>"
            html += f"<p><b>Autor:</b> {job.author}</p>"
            html += f"<p><b>Orçamento:</b> {job.budget}</p>"
            html += f"<p><b>Estrelas:</b> {job.stars}</p>"
            html += f"<p>{job.about.replace(chr(10), '<br>')}</p>"
            html += f"<div class='skills'><b>Skills:</b> {skills_html}</div></div>"

        html += "</body></html>"
        return html
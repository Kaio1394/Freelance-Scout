class EmailError(Exception):
    pass

class EmailConnectionError(EmailError):
    def __init__(self, message: str = "SMTP server is not connected. Call connect() before using this method."):
        super().__init__(message)

class EmailSendError(EmailError):
    def __init__(self, message: str = "Failed to send email. Check server connection and recipient address."):
        super().__init__(message)

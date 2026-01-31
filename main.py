import os
from typing import List
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr

app = FastAPI()

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
    MAIL_FROM=os.environ.get("MAIL_FROM"),
    MAIL_PORT=int(os.environ.get("MAIL_PORT", 587)),
    MAIL_SERVER=os.environ.get("MAIL_SERVER"),
    MAIL_STARTTLS=os.environ.get("MAIL_STARTTLS", "True") == "True",
    MAIL_SSL_TLS=os.environ.get("MAIL_SSL_TLS", "False") == "True",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

@app.post("/send-inquiry")
async def send_inquiry(
    name: str = Form(...),
    phone: str = Form(...),
    email: EmailStr = Form(...),
    inquiry_type: str = Form(...),
    message: str = Form(...),
    files: List[UploadFile] = File(...)
):
    message_body = f"""
    New Inquiry Received:
    Name: {name}
    Phone: {phone}
    Email: {email}
    Type: {inquiry_type}
    Message: {message}
    """

    message_object = MessageSchema(
        subject=f"New Inquiry from {name} - {inquiry_type}",
        recipients=[os.environ.get("MAIL_RECIPIENT")],
        body=message_body,
        subtype=MessageType.plain,
        attachments=files
    )

    fm = FastMail(conf)
    
    await fm.send_message(message_object)

    return {"status": "Email sent successfully"}
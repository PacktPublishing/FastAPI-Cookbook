from celery import Celery
from fastapi import FastAPI

app = FastAPI()


celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@celery.task
def send_email(to, subject, body):
    # Logic to send email
    import time

    time.sleep(10)
    print(
        f"Sending email to {to} with subject '{subject}' and body '{body}'"
    )

@app.post("/send-email/")
async def send_email_view(to: str, subject: str, body: str):
    send_email.delay(to, subject, body)
    return {"message": "Email sent successfully"}
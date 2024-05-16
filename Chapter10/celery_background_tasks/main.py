import logging
from time import sleep

from fastapi import FastAPI
from tqdm import tqdm

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
    logger = logging.getLogger(__name__)
    logger.info(f"email to {to}")
    logger.info(f"subject: {subject}")
    logger.info(f"body: {body}")

    for _ in tqdm(range(100), desc="Sending email"):
        sleep(0.1)


@app.post("/send-email/")
async def send_email_view(
    to: str, subject: str, body: str
):
    send_email.delay(to, subject, body)
    return {"message": "Email sent successfully"}

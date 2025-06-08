# app/main.py

from dotenv import load_dotenv
import os
from fastapi import FastAPI, Form, HTTPException
from email_send import send_email
from check_passwords import check_passwords_in_csv


load_dotenv()  # Load environment variables from .env

app = FastAPI()

@app.post("/check")
def check_credentials(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        # Check password against Pwned Passwords API
        results = check_passwords_in_csv("passwords.csv")
        # Send email summary with breach info and risk score
        # email_sender.send_summary(email)

        email2 = '404notfounders404@gmail.com'
        send_email(email2, results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

check_credentials()
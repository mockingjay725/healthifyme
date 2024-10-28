import streamlit as st
import csv
import bcrypt
import random
import smtplib
from email.mime.text import MIMEText
import logging
from datetime import datetime
import requests
import streamlit.components.v1 as components

# Configure logging (optional)
logging.basicConfig(
    filename="audit_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_activity(username, action):
    log_message = f"Username: {username}, Action: {action}, Timestamp: {datetime.now()}"
    logging.info(log_message)

def send_otp_via_email(receiver_email, otp):
    # ... (Your email sending logic here)
    # Replace with your actual email credentials and SMTP server settings
    # ...
    return True  # Indicate successful sending

def verify_recaptcha(response_token):
    secret_key = '6LczHm4qAAAAADEV3g45fegaQx41_TVzuwqlRrXt'  # Replace with your actual secret key
    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {'secret': secret_key, 'response': response_token}
    response = requests.post(verify_url, data=payload)
    result = response.json()
    return result.get('success', False)

# Title of the app
st.title("Healthify: Secure Health Monitoring with reCAPTCHA and OTP")

# HTML for reCAPTCHA widget
recaptcha_html = '''
<script src="https://www.google.com/recaptcha/api.js"></script>
<div class="g-recaptcha" data-sitekey="6LczHm4qAAAAACXVC7bIqBnx6600xr3hCpicMlPG"></div>
'''

st.header("User Registration")
username = st.text_input("Username")
password = st.text_input("Password", type='password')
email = st.text_input("Email Address")

# Display reCAPTCHA
components.html(recaptcha_html, height=100)

if st.button("Register"):
    recaptcha_response = st.experimental_get_query_params().get("g-recaptcha-response", [None])[0]

    if not recaptcha_response:
        st.error("Please complete the reCAPTCHA challenge.")
    elif not verify_recaptcha(recaptcha_response):
        st.error("reCAPTCHA verification failed. Please try again.")
    else:
        otp = random.randint(100000, 999999)
        otp_sent = send_otp_via_email(email, otp)
        if otp_sent:
            st.success(f"OTP sent to {email}. Please check your email.")
            log_activity(username, "OTP Sent")
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            with open('user.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, hashed_password, email])
                log_activity(username, "User Registered")
        else:
            st.error("Failed to send OTP. Please try again.")

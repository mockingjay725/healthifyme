import streamlit as st
import requests

# Function to verify reCAPTCHA
def verify_recaptcha(response_token):
    secret_key = '6LdJF24qAAAAAJhkw61rBOoP9d_Jv-BqT_mGCkjN'  # Replace with your reCAPTCHA secret key
    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {'secret': secret_key, 'response': response_token}
    response = requests.post(verify_url, data=payload)
    result = response.json()
    return result.get('success', False)

# App title and description
st.title("Simple reCAPTCHA Protected Form")
st.write("This form requires reCAPTCHA verification.")

# Input fields
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# reCAPTCHA response input field
st.write("Please verify that you're not a robot.")
recaptcha_response = st.text_input("Enter reCAPTCHA response token")

# Registration button
if st.button("Register"):
    if not username or not password:
        st.error("Please provide both username and password.")
    elif not verify_recaptcha(recaptcha_response):
        st.error("reCAPTCHA verification failed. Please try again.")
    else:
        st.success("Registration successful!")

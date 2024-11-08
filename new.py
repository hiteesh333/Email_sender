import streamlit as st
import pandas as pd
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import random

# Placeholder function for LLM-based content generation (replace with actual API call if available)
def generate_content(prompt, row):
    # Replace placeholders with actual data
    message = prompt
    for column in row.index:
        placeholder = f"{{{column}}}"
        if placeholder in message:
            message = message.replace(placeholder, str(row[column]))
    return message

# Placeholder function to simulate delivery tracking (replace with actual ESP integration)
def track_delivery_status():
    status = random.choice(["Delivered", "Bounced", "Pending", "Opened"])
    return status

# Streamlit interface
st.title("Advanced Bulk Email Sender with Customization, Scheduling, and Tracking")
st.write("Upload a CSV file with data, configure your email account, and set up personalized email campaigns.")

# CSV Upload
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

# Initialize df to None
df = None

# Load the data if the file is uploaded
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.write(df.head())

        # Auto-detect columns for placeholders
        placeholder_options = [f"{{{col}}}" for col in df.columns]
        st.markdown(f"*Detected Placeholders:* {', '.join(placeholder_options)}")

        # Check for required columns
        required_columns = ['Company Name', 'Email']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            st.stop()
        else:
            st.success("Dataset loaded successfully!")
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        st.stop()

# Proceed only if df is successfully loaded
if df is not None:
    # Email Configuration
    st.sidebar.header("Email Configuration")
    email_sender = st.sidebar.text_input("Your Email Address")
    email_password = st.sidebar.text_input("Your Email Password", type="password")
    smtp_server = st.sidebar.text_input("SMTP Server", value="smtp.gmail.com")
    smtp_port = st.sidebar.number_input("SMTP Port", value=587, step=1)

    # Message Template
    st.subheader("Compose Your Message")
    subject = st.text_input("Email Subject", "Hello from [Your Company]")
    message_template = st.text_area(
        "Email Message Template", 
        "Dear {Contact Person},\n\nWe would like to inform you about our latest product offerings for {Company Name} located in {Location}."
    )

    # Scheduling and Throttling
    st.sidebar.header("Scheduling and Throttling")
    schedule_option = st.sidebar.selectbox("Choose when to send emails", ["Immediately", "Schedule"])
    scheduled_time = None
    if schedule_option == "Schedule":
        scheduled_time = st.sidebar.time_input("Select time to send emails")
    rate_limit = st.sidebar.slider("Emails per Minute (Throttle)", min_value=1, max_value=60, value=10)
    daily_limit = st.sidebar.number_input("Max Emails per Day", min_value=1, max_value=500, value=100)

    # Analytics and Tracking
    st.sidebar.header("Email Analytics")
    sent_count = st.sidebar.empty()
    pending_count = st.sidebar.empty()
    failed_count = st.sidebar.empty()
    response_rate = st.sidebar.empty()

    # Retry logic and failure logging
    failed_emails = []
    cooldown_period = 60  # in seconds
    max_retries = 3

    def send_email_with_backoff(server, email_sender, recipient_email, msg, retries=3):
        delay = 5  # start with a 5-second delay
        for attempt in range(retries):
            try:
                server.sendmail(email_sender, recipient_email, msg.as_string())
                return True
            except smtplib.SMTPException as e:
                st.warning(f"Attempt {attempt + 1} failed for {recipient_email}. Retrying after {delay} seconds.")
                time.sleep(delay)
                delay *= 2  # exponential backoff
        return False

    # Sending Emails
    if st.button("Start Email Campaign"):
        try:
            # Initialize SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_sender, email_password)
            st.info("Successfully logged into email server.")

            # Scheduling Logic
            if schedule_option == "Schedule" and scheduled_time:
                send_time = datetime.datetime.combine(datetime.date.today(), scheduled_time)
                while datetime.datetime.now() < send_time:
                    time.sleep(5)
                st.info("Scheduled time reached. Starting to send emails.")

            total_emails = len(df)
            sent_emails, pending_emails, failed_emails = 0, total_emails, 0
            delivery_statuses = []
            emails_sent_today = 0

            for index, row in df.iterrows():
                # Daily limit check
                if emails_sent_today >= daily_limit:
                    st.warning("Daily email limit reached. Stopping campaign.")
                    break

                # Throttling
                if index > 0 and index % rate_limit == 0:
                    time.sleep(60)  # Pause to respect rate limit

                # Prepare email
                msg = MIMEMultipart()
                msg['From'] = email_sender
                msg['To'] = row['Email']
                msg['Subject'] = subject
                message = generate_content(message_template, row)
                msg.attach(MIMEText(message, 'plain'))

                # Attempt to send email with retry logic
                if send_email_with_backoff(server, email_sender, row['Email'], msg, max_retries):
                    st.success(f"Email sent to {row['Email']}")
                    sent_emails += 1
                    emails_sent_today += 1
                    delivery_statuses.append(track_delivery_status())
                else:
                    st.error(f"Failed to send email to {row['Email']} after {max_retries} retries.")
                    failed_emails.append({"email": row['Email'], "error": "Failed after max retries"})
                    failed_emails += 1

                pending_emails = total_emails - sent_emails - failed_emails

                # Update Analytics
                sent_count.text(f"Total Emails Sent: {sent_emails}")
                pending_count.text(f"Emails Pending: {pending_emails}")
                failed_count.text(f"Emails Failed: {failed_emails}")
                opened_emails = delivery_statuses.count("Opened")
                if sent_emails > 0:
                    response_rate.text(f"Response Rate: {opened_emails / sent_emails:.2%}")

            server.quit()

            # Log failures for user review
            if failed_emails:
                st.warning(f"{len(failed_emails)} emails failed to send. Check log for details.")

        except smtplib.SMTPException as e:
            st.error(f"Failed to connect to the email server: {e}")
        finally:
            server.quit()
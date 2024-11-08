# Email_sender
Bulk Email Sender Application
This repository contains a Bulk Email Sender application built with Streamlit. This app allows you to upload a CSV file of contact information and send customized bulk emails with dynamic placeholders, scheduling, throttling, and analytics tracking. It’s designed to streamline email campaigns with added personalization and rate limiting.

Features
CSV Data Upload: Upload a CSV with details (like name, email, location) to auto-detect columns for email customization.
Dynamic Content Replacement: Use placeholders such as {Name}, {Location}, etc., which will be dynamically replaced in each email based on the uploaded data.
Email Scheduling: Schedule emails to be sent at a specific time or spread them over intervals.
Throttling: Set limits to control the rate of sending emails per minute and per day, helping prevent reaching ESP limits.
Error Handling and Retry: Implements exponential backoff and retry mechanisms to handle temporary email sending issues.
Real-Time Analytics: Track sent, pending, and failed emails, as well as response rates for opened emails.
Setup and Installation
Prerequisites
Python 3.7+ is required.

Install the required packages listed in requirements.txt by running:

bash
Copy code
pip install -r requirements.txt
Running the Application
Clone this repository:

bash
Copy code
git clone https://github.com/yourusername/bulk-email-sender.git
cd bulk-email-sender
Start the Streamlit application:

bash
Copy code
streamlit run app.py
Open the link provided by Streamlit in your browser to access the application.

Using Gmail with Two-Factor Authentication
Why Use 2-Step Verification?
Gmail (and other email providers) require enhanced security to access email accounts from external applications. Using Two-Factor Authentication (2FA) and App Passwords ensures your account remains secure while allowing the app to send emails.

Setting Up 2-Step Verification and App Password for Gmail
Enable 2-Step Verification on your Google account:

Go to your Google Account Security page.
Under "Signing in to Google," select 2-Step Verification and follow the steps to set it up.
Generate an App Password:

After enabling 2-Step Verification, go to App Passwords in the same security settings.
Select Mail as the app and your device as Other.
Click Generate to receive a 16-character password.
Use this password in place of your actual Gmail password when logging into the app.
Note: You may need to re-enter your regular Google password to access the App Passwords section.

CSV File Requirements
The CSV file should have the following columns for placeholders to work:

Email: The recipient's email address.
Other columns for personalization, such as Name, Company, Location, etc.
Example CSV file structure:

csv
Copy code
Name,Email,Location,Company
John Doe,john.doe@example.com,New York,ABC Corp
Jane Smith,jane.smith@example.com,London,XYZ Ltd
Customization Guide
Upload a CSV File: Use the app to upload your CSV file with email and personalized data.
Configure Email Settings:
Input your email address and App Password.
Specify the SMTP server and port (e.g., smtp.gmail.com for Gmail, with port 587).
Compose Your Message:
Use placeholders like {Name}, {Location}, {Company}, which will be automatically replaced with data from each row of the CSV.
Set Schedule and Throttling:
Schedule emails to send immediately or at a specified time.
Use throttling options to limit emails per minute and day, helping to stay within your email provider’s limits.
Start Campaign and Monitor:
Start the campaign and monitor real-time analytics, including sent, pending, failed, and response rate statistics.
Error Handling and Limit Management
Retry Mechanism: Automatically retries failed email attempts with exponential backoff.
Logging Failures: Stores failed email logs for easy review.
Daily and Per-Minute Rate Limits: Set limits to avoid exceeding ESP limits.
Troubleshooting
Authentication Errors: If you encounter authentication issues, ensure 2-Step Verification is enabled and you are using an App Password.
SMTP Errors: Double-check SMTP settings for your email provider (e.g., Gmail, Outlook).
Security and Privacy
All authentication credentials, such as App Passwords, should be kept confidential and not shared.
Use the app in a secure environment to prevent unauthorized access.
License
This project is licensed under the MIT License.

Contact
For questions or support, please reach out to [your email or GitHub contact info].

This README provides setup and usage instructions along with detailed guidance on using two-factor authentication with App Passwords, ensuring secure access to Gmail for sending bulk emails.

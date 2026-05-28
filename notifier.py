import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def send_alert(product_name, current_price, target_price, url):
    try:
        subject = f"Price Drop Alert! 🎉 {product_name}"

        body = f"""
        Good news! Price dropped on your tracked product.

        Product: {product_name}
        Current Price: ₹{current_price}
        Your Target: ₹{target_price}

        Buy now: {url}
        """

        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, EMAIL, msg.as_string())
            print(f"✅ Email sent for {product_name}")

    except Exception as e:
        print(f"❌ Email failed: {e}")
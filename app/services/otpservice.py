import smtplib
from email.message import EmailMessage
from app.config import EMAIL_USERNAME, EMAIL_PASSWORD

#credentials from dotenv missing

def send_otp(received_email, otp):
    # create a connection
    server = None
    try:
        server = smtplib.SMTP("smtp.mail.com", 587)
        server.serverttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        
        # create email message

        msg = EmailMessage()
        msg["sub"] = "Otp For Email Verification"
        msg["From"] = EMAIL_USERNAME
        msg["To"] = received_email
        msg.set_content(f"Your OTP code is: {otp}\n\nThis code will expire in 10 minutes.\nIf you didn't request this code, please ignore this email.")

        # send email
        server.send_message(msg)
        print("otp send successfully" + otp)
        return True
    
    except Exception as e:
        print(f"an exception occur while sending the email {e}")

    finally:
        if server:
            try:
                server.quit()
            except:
                pass

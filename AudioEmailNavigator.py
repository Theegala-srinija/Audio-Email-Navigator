import smtplib
from email.message import EmailMessage
from email.header import decode_header
import werkzeug
import imaplib
import email
import speech_recognition as sr
import pyttsx3
from PIL import Image
import io
from transformers import BlipProcessor, BlipForConditionalGeneration
from pywebio.input import *
from pywebio.output import *
import time
import os
from pywebio import start_server  # Changed to use PyWebIO's start_server method instead of Flask


# Get email and password from environment variables
# Directly assign your email and password here
email_address = 'sriharshithadurgam29@gmail.com'  # Replace with your actual email
password = 'ymfg tkxq qszc obwp'
  # Replace with your actual password

# Your assistant setup
def getStarted():
    put_markdown('# Speaking Email')
    put_image(open(r"C:\Users\srini\OneDrive\Desktop\Voice Assistant.gif", "rb").read(), width="100%")

    #put_image(open("Voice Assistant.gif", "rb").read(), width="100%")  # Image file in the same directory

    put_markdown('### Initializing and getting started...')
    put_processbar('bar')
    for i in range(1, 11):
        set_processbar('bar', i / 10)
        time.sleep(0.1)

    # Initialize speech recognition and text-to-speech engines
    listener = sr.Recognizer()
    engine = pyttsx3.init()

    # Function to speak out text
    def talk(text):
        engine.say(text)
        engine.runAndWait()

    # Function to get speech input
    def get_info(prompt):
        try:
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source, duration=0.5)
                talk(prompt)
                put_text(prompt)
                voice = listener.listen(source, timeout=10, phrase_time_limit=15)  # Increased timeout
                info = listener.recognize_google(voice)
                put_text(info)
                return info.lower()
        except sr.UnknownValueError:
            talk("Sorry, I couldn't understand what you said. Please try again.")
        except sr.RequestError:
            talk("Sorry, I'm unable to access the Google API at the moment. Please try again later.")
        except sr.WaitTimeoutError:
            talk("Sorry, I didn't hear anything. Please try again.")
        return ""

    # Function to send email
    def send_email(receiver, subject, message):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_address, password)

            email_msg = EmailMessage()
            email_msg['From'] = email_address
            email_msg['To'] = receiver
            email_msg['Subject'] = subject
            email_msg.set_content(message)

            server.send_message(email_msg)
            server.quit()

            talk("Your email has been sent successfully.")

        except smtplib.SMTPException as e:
            talk("Sorry, authentication failed. Please check your email and password.")

        except Exception as e:
            talk(f"Sorry, an error occurred while sending the email: {e}")

    # Function to describe an image using a pre-trained model
    def describe_image(image):
        try:
            processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

            inputs = processor(images=image, return_tensors="pt")
            out = model.generate(**inputs)
            description = processor.decode(out[0], skip_special_tokens=True)
            return description
        except Exception as e:
            put_text("Error in describing image: %s" % e)
            return None

    # Function to read emails
    def read_emails():
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(email_address, password)

            mail.select("inbox")
            status, messages = mail.search(None, "ALL")

            email_ids = messages[0].split()
            latest_email_id = email_ids[-1]
            status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    from_ = msg.get("From")
                    talk(f"Subject: {subject}")
                    talk(f"From: {from_}")

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            if "attachment" in content_disposition:
                                filename = part.get_filename()
                                if filename:
                                    put_text("Attachment found: %s" % filename)
                                    talk(f"Attachment: {filename}")
                                    if any(image_type in content_type for image_type in ["image/jpeg", "image/png"]):
                                        image_data = part.get_payload(decode=True)
                                        try:
                                            image = Image.open(io.BytesIO(image_data))
                                            put_text("Image opened: %s" % image)
                                            description = describe_image(image)
                                            if description:
                                                talk(f"The image contains: {description}")
                                            else:
                                                talk("The image content could not be identified.")
                                        except Exception as e:
                                            put_text("Error in opening image: %s" % e)
                            elif content_type == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                talk(f"Body: {body}")
                    else:
                        content_type = msg.get_content_type()
                        if content_type == "text/plain":
                            body = msg.get_payload(decode=True).decode()
                            talk(f"Body: {body}")
            mail.close()
            mail.logout()
        except imaplib.IMAP4.error as e:
            talk(f"Sorry, an error occurred while reading emails: {e}")

    # Function to interactively send an email
    def get_email_info():
        talk('Hi, I am your assistant for today. To whom do you want to send an email?')

        name = get_info("Please say the recipient's name. speak")
        talk(name)
        email_list = {
            'Srinija': 'theegalasrinija@gmail.com',
            'Srinidhi': 'srinidhicheedhalla05@gmail.com',
            'Srinath': 'thipparthi.srinath2020@gmail.com',
            'Akshitha': 'akshithakatkam14@gmail.com',
            'mounika': 'bonothm327@gmail.com',
            'Hepsi': 'hepsiba.inaganti123@gmail.com',
            'Teju' : 'ctejasree580@gmail.com',
            'Chinni' : 'katkamkshitha2@gmail.com',
            'Aishwarya' : 'aishwaryabandi147@gmail.com',
            'Shivani' : 'munugotishivani@gmail.com'
        }
        if name in email_list:
            receiver = email_list[name]
            subject = get_info("What is the subject of your email? speak")
            talk("your subject is")
            talk(subject)
            message = get_info("Tell me the text in your email speak")
            talk("your text is")
            talk(message)

            send_email(receiver, subject, message)

            send_more = get_info("Do you want to send another email? speak")
            talk("you said")
            talk(send_more)
            if 'yes' in send_more:
                get_email_info()
            else:
                talk("Goodbye! Have a great day.")
                talk("thank you boss")
        else:
            talk("Sorry, I couldn't find the recipient in the email list.")

    talk("hii boss")
    talk("Do you want to send an email or read an email?")
    action = get_info("Please say 'send' to send an email or 'read' to read an email.")
    talk(action)
    put_text("Action: %s" % action)
    if 'send' in action:
        put_text("send mail")
        get_email_info()
    elif 'read' in action:
        put_text("read email")
        read_emails()
    else:
        put_text("Didn't understand the action")
        talk("Sorry, I didn't understand. Please say 'send' to send an email or 'read' to read an email.")
# Run the PyWebIO server using start_server method
start_server(getStarted, port=801)

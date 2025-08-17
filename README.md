🔐 Face Recognition Door Lock System

This is a Python-based face recognition system integrated with a solenoid lock and email alerts.
When an authorized face is detected, the door unlocks and a notification with an image is sent to a registered email. 
If the face doesn't match, the system captures the image and alerts via email that access was denied.


📸 How It Works

Webcam captures a face when a key is pressed.

The captured face is compared with a set of reference images.

If a match is found:

A solenoid lock is triggered to open the door.

An email with the captured face is sent.

If not matched:

The image is still saved.

An email is sent stating unauthorized access.


🧠 Technologies Used

Python

OpenCV – for webcam and image processing

face_recognition – for face encoding and comparison

NumPy – for vector operations

smtplib / email.mime – to send email with image attachments

dotenv – to manage environment variables

msvcrt – for keypress detection (Windows)

Hardware: Solenoid Lock, Relay Module (optional setup not included in this repo)


🧰 Hardware Used

Webcam

Solenoid Lock

Relay Module

Laptop with USB port

(You can connect solenoid to GPIO pins via Arduino or Raspberry Pi for real setup)


📂 Project Structure

ProjectDoor/

│

├── AuthorizedImages/        # Reference images of authorized users

├── CapturedFace/            # Stores images of detected faces

├── .env                     # Contains email credentials

├── face_recognition_door.py # Main Python script

└── README.md                # This file


🛠️ Setup Instructions

1. Clone the repository

git clone https://github.com/Adwaitha0/faceRecognition.git

cd ProjectDoor

2. Install dependencies

pip install opencv-python face_recognition python-dotenv numpy

3.Add your .env file

Create a file named .env in the root folder with:

SENDER_EMAIL=youremail@gmail.com

SENDER_PASSWORD=yourapppassword

Use App Passwords if 2-step verification is enabled.

4. Add authorized images

Place face images of authorized people inside the AuthorizedImages/ folder. Name them meaningfully (e.g., referenceface1.jpg).

5. Run the app

python face_recognition_door.py

Then press any key to capture a face. Press q to quit.


🔐 Solenoid Lock Integration

The script can be modified to control GPIO pins on Raspberry Pi or communicate with an Arduino to trigger a relay module connected to a solenoid lock.

Example (Raspberry Pi):

import RPi.GPIO as GPIO

GPIO.output(RELAY_PIN, GPIO.HIGH)  # To unlock

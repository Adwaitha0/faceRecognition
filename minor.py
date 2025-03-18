import cv2
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import face_recognition
import numpy as np
import msvcrt

load_dotenv()
# Path to the reference face images
reference_images = [
    'C:\\Users\\X2\\Desktop\\ProjectDoor\\AuthorizedImages\\referenceface1.jpg',
    'C:\\Users\\X2\\Desktop\\ProjectDoor\\AuthorizedImages\\referenceface2.jpg',
    'C:\\Users\\X2\\Desktop\\ProjectDoor\\AuthorizedImages\\referenceface3.jpg',
    'C:\\Users\\X2\\Desktop\\ProjectDoor\\AuthorizedImages\\referenceface4.jpg',
]

matching_threshold = 0.56

def load_reference_faces():
    reference_face_images = []

    for image_path in reference_images:
        reference_image = face_recognition.load_image_file(image_path)
        reference_face_encoding = face_recognition.face_encodings(reference_image)[0]
        reference_face_images.append(reference_face_encoding)
    return reference_face_images

def capture_face_webcam(video_capture):
    while True:
        # Capture a frame
        ret, frame = video_capture.read()

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)

        # Check if a face is detected
        if len(face_locations) > 0:
            # Extract the face region
            top, right, bottom, left = face_locations[0]
            face = rgb_frame[top:bottom, left:right]

            # Resize the face to the desired dimensions
            face = cv2.resize(face, (160, 160))

            # Convert the face to RGB format
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

            # Return the captured frame and face image
            return frame, face

        # Display the frame without a face
        cv2.imshow("No Face Detected", frame)

        # Wait for a key press to exit or continue capturing
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Close all windows
    cv2.destroyAllWindows()

def send_email_with_image(image_path, result):
    # Email configurations    
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = 'facelog559@gmail.com'

    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = result

    # Attach the image to the email
    with open(image_path, 'rb') as fp:
        img = MIMEImage(fp.read())
    msg.attach(img)

    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print('Email sent successfully!')
    except Exception as e:
        print('Failed to send email:', str(e))

# Initialize the webcam
video_capture = cv2.VideoCapture(0)

while True:
    print("Press any key to capture a face from the webcam...")
    key = msvcrt.getch()
    if key == b'q' :
        exit()

    # Capture the image and detect a face
    captured_frame, captured_face = capture_face_webcam(video_capture)

    if captured_face is not None:
        print('Face is detected.')

        # Load the reference face encodings
        reference_faces = load_reference_faces()

        # Compare the captured face with reference faces
        captured_face_encodings = face_recognition.face_encodings(captured_face)
        if len(captured_face_encodings) > 0:
            captured_face_encoding = captured_face_encodings[0]

            similarities = face_recognition.face_distance(reference_faces, captured_face_encoding)

            for i, similarity in enumerate(similarities):
                print(f"Un-Similarity with reference image {i+1}: {similarity:.2f}%")

            # Find the index of the best matching reference face
            best_match_index = np.argmin(similarities)
            best_match_value = similarities[best_match_index]

            # Check if the best match is below the threshold
            if best_match_value <= matching_threshold:
                print("Door opens!")
                result = "Face Matched"
                # Save the captured frame
                image_path = 'C:\\Users\\X2\\Desktop\\ProjectDoor\\CapturedFace\\captured_face.jpg'
                cv2.imwrite(image_path, captured_frame)

                # Send the email with the captured image
                send_email_with_image(image_path, result)

                print('Face matched with reference image:', reference_images[best_match_index])
            else:
                image_path = 'C:\\Users\\X2\\Desktop\\ProjectDoor\\CapturedFace\\captured_face.jpg'
                cv2.imwrite(image_path, captured_frame)
                result = "Face does not Match"
                send_email_with_image(image_path, result)
                print('No face match found.')
        else:
            print('No face encodings found for the captured face.')
    else:
        print('No face detected.')
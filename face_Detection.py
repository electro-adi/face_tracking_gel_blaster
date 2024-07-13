import serial
import time
import math
import cv2
import pygame

pygame.mixer.init()

beep = pygame.mixer.Sound(r'C:\Users\Downloads\target_lock.mp3')

ser = serial.Serial('COM3', 9600)
ex = 0
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
capture = cv2.VideoCapture(0)#camera device id here
tp = 300
ty = 315
detected = 0


def send_coordinates_to_arduino(x, y, detected):
    # Convert the coordinates to a string and send it to Arduino
    coordinates = f"{x},{y},{detected}\r"
    ser.write(coordinates.encode())
    print(f"{x},{y},{detected}\n")


while True:
    ret, img = capture.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        ty = x + math.floor(w / 2)
        tp = y + math.floor((7 * h) / 20)

    length_of_soundfile = beep.get_length()

    if len(faces) > 0 and not pygame.mixer.get_busy():
        start_time = time.time()
        beep.play()
    elif len(faces) == 0:
        beep.stop()
        detected = 0

    
    if pygame.mixer.get_busy() and len(faces) > 0:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= length_of_soundfile - 0.8:
            if len(faces) > 0:
                detected = 1



    sendy = str(math.floor(ty * (-45 / 573) + 117.9))
    sendp = str(math.floor(tp * (-45 / 470) + 75))

    send_coordinates_to_arduino(sendy, sendp, detected)


    cv2.imshow('Video', img)

    if cv2.waitKey(20) & 0xFF == ord('d'):
       break

capture.release()
cv2.destroyAllWindows()

"""
Capture frames from a camera using openCV and publish on an MQTT topic.
"""
import time
import os
import cv2
import datetime

from mqtt import get_mqtt_client
from helpers import pil_image_to_byte_array, get_now_string, get_config
from imutils.video import WebcamVideoStream
from imutils import opencv2matplotlib

from PIL import Image

print(os.getenv("MQTT_CAMERA_CONFIG"))
CONFIG_FILE_PATH = os.getenv("MQTT_CAMERA_CONFIG", "./config/config.yml")
# CONFIG_FILE_PATH = "./config/config.yml"
CONFIG = get_config(CONFIG_FILE_PATH)

MQTT_BROKER = CONFIG["mqtt"]["broker"]
MQTT_PORT = CONFIG["mqtt"]["port"]
MQTT_QOS = CONFIG["mqtt"]["QOS"]
MQTT_USER = CONFIG["mqtt"]["username"]
MQTT_PWD = CONFIG["mqtt"]["password"]

MQTT_TOPIC_CAMERA = CONFIG["camera"]["mqtt_topic"]
VIDEO_SOURCE = CONFIG["camera"]["vide_source"]
FPS = CONFIG["camera"]["fps"]


def main():
    client = get_mqtt_client()
    if MQTT_USER != "" and MQTT_PWD != "":
        client.username_pw_set(MQTT_USER, MQTT_PWD)
    client.connect(MQTT_BROKER, port=MQTT_PORT)
    time.sleep(4)  # Wait for connection setup to complete
    client.loop_start()

    # Open camera
    camera = WebcamVideoStream(src=VIDEO_SOURCE).start()
    time.sleep(2)  # Webcam light should come on if using one

    while True:
        frame = camera.read()

        font = cv2.FONT_HERSHEY_SIMPLEX
        datet = str(datetime.datetime.now())
        frame = cv2.putText(frame, datet, (10, 100), font, 1,(0, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame)

        np_array_RGB = opencv2matplotlib(frame)  # Convert to RGB

        image = Image.fromarray(np_array_RGB)  #  PIL image
        byte_array = pil_image_to_byte_array(image)
        client.publish(MQTT_TOPIC_CAMERA, byte_array, qos=MQTT_QOS)
        now = get_now_string()
        print(f"published frame on topic: {MQTT_TOPIC_CAMERA} at {now}")
        time.sleep(1 / FPS)


if __name__ == "__main__":
    main()

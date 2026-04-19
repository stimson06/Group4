"""
This code will help us capture the dataset required for handset detection.

Make sure to update the sample and sample_number to collect them appropriately

Dataset collection numbering
1-20 Abhishek
21-40 Stimson
41-60 Parikshit
61-80 Ryan
81-100 Musab
"""

# Snapshot.py
import sensor
import time
import os
from machine import LED


sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
sensor.set_hmirror(1) # horizontal mirror for proper directions


# Initalizing vairables
class_name = 'left'  # right, forward, backward
samples = 20  # samples to collect 
delay = 2000  # 2 seconds
sample_number = 20  # Dataset numbering (use the starting number) I've used 20 to collect data from class_20 - class_40


# Creating dir
current_dir = os.getcwd()
folder_name = 'handset_dataset'
if not folder_name in os.listdir(current_dir):
    os.mkdir(folder_name)
    print(f"Folder created at: {current_dir}/{folder_name}")
else:
    print(f"Folder already exists at: {current_dir}/{folder_name}")
save_root_path = f"{current_dir}/{folder_name}/"

print(f"Starting to capture images for {class_name}")

red = LED("LED_RED")  # for waiting period
green = LED("LED_GREEN")  # for capturing
time.sleep_ms(delay)

# Capturing loop
for i in range(1, samples+1):
    red.off()
    green.on()

    # capture
    img = sensor.snapshot()

    img_name = f"{class_name}_{sample_number+i}.jpg"

    # Save the image to dataset
    file_path = save_root_path+img_name

    img.save(file_path)
    print(f"Saved: {file_path}")

    green.off()
    red.on()
    time.sleep_ms(delay)

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

import sensor
import time
import os
import gc
from machine import LED

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_hmirror(1)

# Initializing variables
class_name = 'left'   # change to: right, forward, backward
samples = 20
sample_number = 80    # Musab: 80+1=81 ... 80+20=100

countdown_blinks = 3 # No. of Blinks the LED does before the photo is taken
blink_interval   = 500 # Time interval btwn Blinks in ms
green_flash      = 300 # How long Green Blink happens in the LED post capture 

# Creating dir & file handeling to ensure file are not corrupt on write 
current_dir = os.getcwd()
folder_name = 'handset_dataset'
if not folder_name in os.listdir(current_dir):
    os.mkdir(folder_name)
    print(f"Folder created at: {current_dir}/{folder_name}")
else:
    print(f"Folder already exists at: {current_dir}/{folder_name}")
save_root_path = f"{current_dir}/{folder_name}/"

# Print statements to terminal for clarity while taking photos  
print(f"\nStarting capture for class : {class_name}")
print(f"Saving                     : {class_name}_{sample_number+1}.jpg  -->  {class_name}_{sample_number+samples}.jpg")
print(f"Countdown                  : {countdown_blinks} red blinks then capture\n")

red   = LED("LED_RED")
green = LED("LED_GREEN")

red.off()
green.off()
time.sleep_ms(2000)

for i in range(1, samples + 1):

    print(f"Image {i}/{samples} -- get your hand in position...")

    # Countdown blinks on red LED
    for blink in range(countdown_blinks):
        red.on()
        time.sleep_ms(blink_interval)
        red.off()
        time.sleep_ms(blink_interval)

    # Capture
    green.on()
    img = sensor.snapshot()
    img_name = f"{class_name}_{sample_number + i}.jpg"
    file_path = save_root_path + img_name

    # Write image using explicit file handle so we can flush properly
    with open(file_path, 'wb') as f:
        buf = img.compress(quality=85)
        f.write(buf)
        f.flush()           # flush write buffer to filesystem layer

    os.sync()              # commit filesystem to flash storage
    gc.collect()           # free memory immediately

    print(f"Saved + synced : {img_name}  ({i}/{samples})")

    time.sleep_ms(green_flash)
    green.off()

    time.sleep_ms(1500)

# Final sync at the end cause it doesnt hurt to be safe
os.sync()

red.off()
green.off()
print(f"\nAll {samples} images captured for class: {class_name}")
print("Safe to disconnect or access drive now.")
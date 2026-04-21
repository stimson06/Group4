#if anyone have problem saving pictures try this code after changing sample number.
#I had some issues with the saving file.
import sensor
import time
import os
from machine import LED

# Camera setup
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

# Dataset settings
class_name = "unknown"  # left, right, forward, backward, unknown
samples = 20             # Ryan: 20 samples
delay = 5000             # 5 seconds
sample_number = 0        # Ryan starts from 61

# Save folder in internal flash
save_dir = "/flash/handset_dataset"

# LEDs
red = LED("LED_RED")
green = LED("LED_GREEN")

# Create folder if it doesn't exist
try:
    os.stat(save_dir)
except OSError:
    os.mkdir(save_dir)

print("Starting capture for", class_name)

red.on()
green.off()
time.sleep_ms(delay)

for i in range(1, samples + 1):
    red.off()
    green.on()

    img = sensor.snapshot()

    img_name = "%s_%d.jpg" % (class_name, sample_number + i)
    file_path = save_dir + "/" + img_name

    img.save(file_path)
    print("Saved:", file_path)

    green.off()
    red.on()
    time.sleep_ms(2000)

print("Done")
green.off()
red.off()

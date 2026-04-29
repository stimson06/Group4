import sensor, time, ml, uos, gc
import math, network, socket

# ── WiFi ──────────────────────────────────────────────────────────────────────
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("S10e", "123456789")
print("Connecting to WiFi...")
while not wlan.isconnected():
    time.sleep_ms(100)
print("Connected! IP:", wlan.ifconfig()[0])

ESP32_IP   = "192.168.137.109"
ESP32_PORT = 5005
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ── Camera ────────────────────────────────────────────────────────────────────
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240, 240))       # matches Edge Impulse training
sensor.skip_frames(time=2000)

# ── Load model + labels ───────────────────────────────────────────────────────
try:
    net = ml.Model("/flash/trained_5_class.tflite",
                   load_to_fb=uos.stat("/flash/trained_5_class.tflite")[6] > (gc.mem_free() - (64*1024)))
    print("Model loaded!")
except Exception as e:
    raise Exception("Failed to load trained.tflite: " + str(e))

try:
    labels = [line.rstrip("\n") for line in open("labels.txt")]
    print("Labels:", labels)
except Exception as e:
    raise Exception("Failed to load labels.txt: " + str(e))

# ── Main loop ─────────────────────────────────────────────────────────────────
last_sent = ""
clock = time.clock()

while True:
    clock.tick()
    img = sensor.snapshot()

    predictions = list(zip(labels, net.predict([img])[0].flatten().tolist()))

    # Get top prediction
    top_label, top_conf = max(predictions, key=lambda x: x[1])

    # Print all scores
    for label, conf in predictions:
        print("%s = %.2f" % (label, conf))
    print(">> TOP: " + top_label + "  " + str(round(top_conf*100)) + "%  " + str(round(clock.fps(),1)) + "fps")
    print()

    # Send to ESP32 only if confident and changed
    if top_label != last_sent and top_conf > 0.6 and top_label != "unknown":
        try:
            udp.sendto(top_label.encode(), (ESP32_IP, ESP32_PORT))
            last_sent = top_label
            print("Sent to ESP32: " + top_label)
        except Exception as e:
            print("WiFi error: " + str(e))

    # Frame buffer overlay
    color = (0, 255, 0) if top_conf > 0.6 else (255, 165, 0)
    img.draw_string(2, 2,  top_label,                      color=color,         scale=3)
    img.draw_string(2, 40, str(round(top_conf*100)) + "%", color=(255, 255, 0), scale=2)
    img.draw_string(2, 70, str(round(clock.fps(),1)) + "fps", color=(200,200,200), scale=1)

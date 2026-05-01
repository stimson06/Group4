# =============================================================
# Gesture Detection — OpenMV RT1062 Deployment Script
# Model : gesture_cnn_int8_tfl2.tflite (INT8, ~102KB)
# Classes: backward, forward, left, right, unknown
# Hardware: OpenMV RT1062 + 4x LED breadboard (active-low)
# Firmware: OpenMV v4.8.1 / MicroPython v1.26.0-77
# =============================================================

import sensor, ml, ml.preprocessing
import time, math, machine, gc

# ── GPIO (active-low: value(0) = LED ON, value(1) = LED OFF) ──
# Anodes → 3.3V rail, cathodes → GPIO pins via 330Ω resistors
led_left     = machine.Pin("P0", machine.Pin.OUT)  # Grey   → Left LED
led_backward = machine.Pin("P1", machine.Pin.OUT)  # Yellow → Bottom LED
led_forward  = machine.Pin("P2", machine.Pin.OUT)  # Red    → Top LED
led_right    = machine.Pin("P3", machine.Pin.OUT)  # Orange → Right LED

def all_off():
    led_left.value(1)
    led_backward.value(1)
    led_forward.value(1)
    led_right.value(1)

# ── Camera ────────────────────────────────────────────────────
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.B64X64)   # 64x64 — closest to 48x48 training input
sensor.set_hmirror(1)                 # mirror so left/right map correctly
sensor.skip_frames(time=2000)

# ── Model ─────────────────────────────────────────────────────
# Class order must match training: alphabetical (ImageDataGenerator default)
# backward=0, forward=1, left=2, right=3, unknown=4
LABELS     = ["backward", "forward", "left", "right", "unknown"]
CONFIDENCE = 0.6    # minimum probability to trigger an LED

gc.collect()
print("Free RAM before load:", gc.mem_free(), "bytes")

model = ml.Model("/flash/gesture_cnn_int8_tfl2.tflite", load_to_fb=False)

print("Model loaded OK")
print("Free RAM after load :", gc.mem_free(), "bytes")

# ── Normalisation (0-255 → 0.0-1.0, matches training rescale=1./255) ──
norm = ml.preprocessing.Normalization(scale=(0.0, 1.0))

# ── Softmax ───────────────────────────────────────────────────
def softmax(x):
    m = max(x)
    e = [math.exp(v - m) for v in x]
    s = sum(e)
    return [v / s for v in e]

# ── Startup ───────────────────────────────────────────────────
all_off()
clock = time.clock()
print("Ready — running gesture detection")
print("Classes:", LABELS)
print("Confidence threshold:", CONFIDENCE)

# ── Inference loop ────────────────────────────────────────────
while True:
    clock.tick()

    img   = sensor.snapshot()
    out   = model.predict([norm(img)])[0].flatten().tolist()
    probs = softmax(out)
    idx   = probs.index(max(probs))
    conf  = probs[idx]
    label = LABELS[idx]

    all_off()

    if conf >= CONFIDENCE:
        if   label == "left":     led_left.value(0)
        elif label == "right":    led_right.value(0)
        elif label == "forward":  led_forward.value(0)
        elif label == "backward": led_backward.value(0)
        # unknown → all LEDs stay off

    print(label, str(round(conf * 100)) + "%", str(round(clock.fps(), 1)) + " fps")

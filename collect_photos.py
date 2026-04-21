"""
Gesture Photo Collection Script
================================
Naming convention:
  Photos 1-20:   Abhishek
  Photos 21-40:  Stimson
  Photos 41-60:  Parikshit  ← your range
  Photos 61-80:  Ryan
  Photos 81-100: Musab

Gestures: left, right, forward, backward
Each photo saved as: <gesture>_<global_index:02d>.jpg
  e.g. left_41.jpg, right_42.jpg  (for Parikshit)
"""

import cv2
import os
import sys

# ── Name → photo index range mapping ──────────────────────────────────────────
NAME_RANGES = {
    "abhishek":  (1,  20),
    "stimson":   (21, 40),
    "parikshit": (41, 60),
    "ryan":      (61, 80),
    "musab":     (81, 100),
}

GESTURES = ["left", "right", "forward", "backward"]


def get_name_and_range():
    """Prompt for name and return (name, start, end)."""
    print("\n╔══════════════════════════════════════╗")
    print("):
        print(f"  {name.capitalize():12s}  →  photos {s:02d}–{e:02d}")

    print()
    while True:
        name_input = input("Enter your name: ").strip().lower()
        if name_input in NAME_RANGES:
            start, end = NAME_RANGES[name_input]
            print(f"\n✓ Welcome, {name_input.capitalize()}!")
            print(f"  Your photo range: {start} – {end}  ({end - start tos total)\n")
            return name_input, start, end
        else:
            print(f"  ✗ '{name_input}' not found. Choose from: {', '.join(NAME_RANGES.keys())}")


def select_gesture():
    """Let user pick which gesture to collect."""
    print("Select gesture to collect:")
    for i, g in enumerate(GESTURES, 1):
        print(f"  {i}. {g}")
    print("  5. Collect ALL gestures in sequence")
    print()
    while True:
        choice = input("Enter choice (1-5): ").strip()
        if choice in ("1", "2", "3", "4"):
            return [GESTURES[int(choice) - 1]]
        elif choice == "5":
            return GESTURES
        else:
            print("  Please enter 1–5.")


def p_output_dir(name: str) -> str:
    """Create output directory: ./dataset/<Name>/"""
    out_dir = os.path.join("dataset", name.capitalize())
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def collect_gesture_photos(gesture: str, start_idx: int, end_idx: int,
                            out_dir: str, cap: cv2.VideoCapture):
    """
    Collect photos for one gesture.
    Photos are numbered globally (start_idx to end_idx).
    Each gesture gets its own sequential _01, _02, … suffix within the range.
    """
    total = end_idx - start_idx + 1          # 20 photos per person
    per_gesture = total // len(GESTURES)     # 5 photos per gesture (20÷4)

    # Determine which slot within the global range this gesture occupies
    gesture_idx = GESTURES.index(gesture)
    global_start = start_idx + gesture_idx * per_gesture

    print(f"\n── Collecting: {gesture.upper()} ──")
    print(f"   Global indices: {g} – {global_start + per_gesture - 1}")
    print(f"   Saved as:  {gesture}_01.jpg … {gesture}_{per_gesture:02d}.jpg")
    print(f"   Press ENTER to capture, 'q' + ENTER to quit this gesture.\n")

    captured = 0
    while captured < per_gesture:
        ret, frame = cap.read()
        if not ret:
            print("  ✗ Camera read failed. Check connection.")
            break

        # Show live preview with overlay
        display = frame.copy()
        cv2.putText(display, f"Gesture: {gesture.upper()}", (10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        cv2.putText(display, f"Photo {captured + 1}/{per_gesture}", (10, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)
        cv2.putText(display, "Press ENTER to capture | Q to skip gesture",
                    (10, display.shape[0] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)
        cv2.imshow("Gesture Collection", display)

        key = cv2.waitKey(1) & 0      if key == ord('q'):
            print(f"  Skipping rest of {gesture}.")
            break
        elif key == 13:  # ENTER key in OpenCV window
            photo_num = captured + 1
            filename = f"{gesture}_{photo_num:02d}.jpg"
            filepath = os.path.join(out_dir, filename)
            cv2.imwrite(filepath, frame)
            captured += 1
            print(f"  ✓ Saved: {filepath}  ({captured}/{per_gesture})")

    print(f"\n  Completed {captured}/{per_gesture} photos for '{gesture}'.")
    return captured


def collect_gesture_photos_terminal(gesture: str, start_idx: int, end_idx: int,
                                     out_dir: str, cap: cv2.VideoCapture):
    """
    Terminal-mode: press ENTER in terminal to capture (not in OpenCV window).
    Falls back if OpenCV window interaction isn't working.
    """
    total = end_idx - start_idx + 1
    per_gesture = total // len(GESTURES)
    gesture_idx = GESTURES.index(gesture)
    global_start = start_idx + gesture_idx * per_gesture    print(f"\n── Collecting: {gesture.upper()} ──")
    print(f"   {per_gesture} photos needed (global {global_start}–{global_start + per_gesture - 1})")

    captured = 0
    while captured < per_gesture:
        user_in = input(f"  [{gesture} {captured + 1}/{per_gesture}] Press ENTER to capture (or type 'q' to skip): ").strip().lower()
        if user_in == 'q':
            print(f"  Skipping rest of {gesture}.")
            break

       e = cap.read()
        if not ret:
            print("  ✗ Camera read failed.")
            break

        photo_num = captured + 1
        filename = f"{gesture}_{photo_num:02d}.jpg"
        filepath = os.path.join(out_dir, filename)
        cv2.imwrite(filepath, frame)
        captured += 1
        print(f"  ✓ Saved: {filepath}")

    return captured


def main():
    # ── 1. Get user info ──────────────────────────────────────────────────────
    name, start_idx, end_idx = get_name_and_range()
    out_dir = setup_output_dir(name)

    # ── 2. Choose gesture(s) ─────────────────────────────────────────────────
    gestures_to_collect = select_gesture()

    # ── 3. Open camera ─────────────────────────────────────nt("✓ Camera ready.\n")

    # ── 4. Detect mode: OpenCV window vs terminal ─────────────────────────────
    mode = input("Mode: (1) OpenCV window preview  (2) Terminal ENTER only [default: 1]: ").strip()
    use_terminal = (mode == "2")

    # ── 5. Collect ───────────────────────────────────────────────────────────
    total_captured = 0
    for gesture in gestures_to_collect:
        if use_terminal:
            n = collect_gesture_photos_terminal(gesture, start_idx, end_idx, out_dir, cap)
        else:
            n = collect_gesture_photos(gesture, start_idx, end_idx, out_dir, cap)
        total_captured += n

    # ── 6. Done ───────────────────────────────────────────────────────────────
  Photos : {str(total_captured):27s}║")
    print("╚══════════════════════════════════════╝\n")

    # List what was saved
    files = sorted(os.listdir(out_dir))
    if files:
        print("Files saved:")
        for f in files:
            print(f"  {f}")


if __name__ == "__main__":
    main()

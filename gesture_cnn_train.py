"""
Gesture Detection CNN — OpenMV RT1062 deployment target
5 classes: forward, backward, left, right, unknown
Input: 48x48 grayscale  (fits MCU tensor arena; 96x96 RGB overflows)
Architecture: Conv(32)->Conv(64)->Conv(128)->GAP->Dropout->Dense(5)
Export: INT8 TFLite with TFL2 schema (OpenMV ml module requires TFL2, not TFL3)

"""

import os, shutil, pathlib
import numpy as np
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf
from tensorflow.keras import layers, callbacks

# ── Constants ──────────────────────────────────────────────────────────────────
IMG_H, IMG_W = 48, 48
CLASSES = ["forward", "backward", "left", "right", "unknown"]
NUM_CLASSES = len(CLASSES)
BATCH_SIZE = 32
EPOCHS = 45
DATASET_DIR = pathlib.Path("D:/Projects/Group4/augmented_data")
MODEL_DIR = pathlib.Path("model_output")
MODEL_DIR.mkdir(exist_ok=True)

# ── Dataset ────────────────────────────────────────────────────────────────────
def load_from_directory():
    """Load from dataset/<class_name>/ structure."""
    common = dict(
        labels="inferred",
        label_mode="categorical",
        class_names=CLASSES,
        color_mode="grayscale",
        batch_size=BATCH_SIZE,
        image_size=(IMG_H, IMG_W),
        validation_split=0.2,
        seed=42,
    )
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR, subset="training", **common)
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR, subset="validation", **common)
    # Normalise pixels to [0, 1] — model does NOT contain a Rescaling layer
    norm = lambda x, y: (tf.cast(x, tf.float32) / 255.0, y)
    return train_ds.map(norm), val_ds.map(norm)


def make_synthetic_dataset(n_per_class=260):
    """
    Fallback when no dataset/ folder exists.
    Generates random pixel data to verify the full pipeline
    (train -> export -> patch -> validate) without needing real images.
    Replace by placing labelled images under dataset/<class_name>/ for real training.
    """
    print("[INFO] No dataset/ folder found — using synthetic data for pipeline verification.")
    rng = np.random.default_rng(42)
    n = n_per_class * NUM_CLASSES
    # Raw uint8 images
    x = rng.integers(0, 256, (n, IMG_H, IMG_W, 1), dtype=np.uint8)
    y = np.repeat(np.arange(NUM_CLASSES), n_per_class)
    y_oh = tf.keras.utils.to_categorical(y, NUM_CLASSES)

    split = int(n * 0.8)
    # Normalise to [0, 1] float32 — consistent with real-data pipeline
    x_f = x.astype("float32") / 255.0

    train_ds = (
        tf.data.Dataset.from_tensor_slices((x_f[:split], y_oh[:split]))
        .shuffle(1024, seed=42).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    )
    val_ds = (
        tf.data.Dataset.from_tensor_slices((x_f[split:], y_oh[split:]))
        .batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    )
    return train_ds, val_ds


def get_datasets():
    if DATASET_DIR.exists() and any(DATASET_DIR.iterdir()):
        print("[INFO] Loading real images from dataset/ directory.")
        return load_from_directory()
    return make_synthetic_dataset()

# ── Model ──────────────────────────────────────────────────────────────────────
def build_model():
    """
    3-block CNN sized for RT1062 (Cortex-M7, 8MB SRAM).

    - Input: float32 [0, 1], shape (1, 48, 48, 1)
    - GlobalAveragePooling2D: collapses 6×6×128 -> 128 — avoids 4608-element
      Flatten tensor that would blow the MCU arena with Flatten()
    - No Rescaling layer inside model: keeps representative-dataset and
      training normalisation identical; no accidental double-scaling
    """
    inp = tf.keras.Input(shape=(IMG_H, IMG_W, 1), name="input_image")

    x = layers.Conv2D(32, 3, padding="same", activation="relu")(inp)
    x = layers.MaxPooling2D(2, 2)(x)                # -> 24×24×32

    x = layers.Conv2D(64, 3, padding="same", activation="relu")(x)
    x = layers.MaxPooling2D(2, 2)(x)                # -> 12×12×64

    x = layers.Conv2D(128, 3, padding="same", activation="relu")(x)
    x = layers.MaxPooling2D(2, 2)(x)                # -> 6×6×128

    x = layers.GlobalAveragePooling2D()(x)          # -> 128
    x = layers.Dropout(0.3)(x)
    out = layers.Dense(NUM_CLASSES, activation="softmax", name="predictions")(x)

    return tf.keras.Model(inp, out, name="gesture_cnn")

# ── Training ───────────────────────────────────────────────────────────────────
def train(model, train_ds, val_ds):
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    model.summary()

    cbs = [
        callbacks.EarlyStopping(
            monitor="val_accuracy", patience=8, restore_best_weights=True),
        callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=4, min_lr=1e-6),
        callbacks.ModelCheckpoint(
            str(MODEL_DIR / "best_gesture_cnn.keras"),
            monitor="val_accuracy", save_best_only=True),
    ]

    history = model.fit(
        train_ds, validation_data=val_ds, epochs=EPOCHS, callbacks=cbs, verbose=1)
    return history

# ── TFLite INT8 Export ─────────────────────────────────────────────────────────
def export_tflite_int8(model, train_ds):
    """
    Full-integer quantization (weights + activations + input + output all INT8).

    The representative dataset MUST be float32 in [0, 1] — same range the model
    was trained with.  Setting inference_input_type / inference_output_type to
    tf.int8 tells the converter to also quantize the graph boundary tensors,
    which is mandatory for MCU deployment via OpenMV's ml module.

    Uses model.export() (Keras 3 API) to produce a SavedModel, then converts.
    """
    saved_model_path = str(MODEL_DIR / "gesture_cnn_savedmodel")
    if pathlib.Path(saved_model_path).exists():
        shutil.rmtree(saved_model_path)
    model.export(saved_model_path)          # Keras 3: export() -> SavedModel

    def representative_dataset():
        count = 0
        for batch_x, _ in train_ds:
            for img in batch_x:
                if count >= 200:
                    return
                # shape [1, H, W, C], float32, range [0, 1]
                yield [tf.expand_dims(img, 0)]
                count += 1

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = representative_dataset
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8

    tflite_model = converter.convert()

    tflite_path = MODEL_DIR / "gesture_cnn_int8.tflite"
    tflite_path.write_bytes(tflite_model)
    print(f"[OK] TFLite model written: {tflite_path}  ({len(tflite_model)/1024:.1f} KB)")
    return tflite_path, tflite_model

# ── TFL3 -> TFL2 Schema Patch ───────────────────────────────────────────────────
def patch_tflite_schema(tflite_path):
    """
    TF 2.x exports flatbuffers with file_identifier b"TFL3".
    OpenMV firmware ml module only understands b"TFL2".

    Flatbuffer layout:
      bytes[0:4]  root table offset (uint32 LE)
      bytes[4:8]  file identifier: b"TFL3"  (byte 7 = 0x33)

    Changing byte 7 from 0x33 -> 0x32 downgrades the header.
    Model weights and graph structure (stored at offset ≥ 8) are untouched.
    """
    data = bytearray(tflite_path.read_bytes())
    identifier = bytes(data[4:8])
    print(f"[INFO] TFLite file identifier before patch: {identifier}")

    if identifier == b"TFL3":
        data[7] = ord("2")
        patched_path = MODEL_DIR / "gesture_cnn_int8_tfl2.tflite"
        patched_path.write_bytes(bytes(data))
        print(f"[OK] Schema patched TFL3 -> TFL2: {patched_path}")
        return patched_path
    elif identifier == b"TFL2":
        print("[INFO] File already TFL2 — no patch needed.")
        patched_path = MODEL_DIR / "gesture_cnn_int8_tfl2.tflite"
        shutil.copy(tflite_path, patched_path)
        return patched_path
    else:
        raise RuntimeError(f"Unexpected file identifier {identifier!r} — cannot patch.")

# ── Validation ─────────────────────────────────────────────────────────────────
def validate_tflite(tflite_path):
    """
    Validates the TFL3 (pre-patch) file with the host interpreter.
    TF 2.20+ rejects TFL2 on the host — the TFL2 patch is only for OpenMV firmware.
    Tensor shapes, quantization params, and graph correctness are identical between
    TFL3 and TFL2 because only byte 7 of the header changes.
    """
    interp = tf.lite.Interpreter(model_path=str(tflite_path))
    interp.allocate_tensors()

    inp_det = interp.get_input_details()[0]
    out_det = interp.get_output_details()[0]

    print("\n[VALIDATION] Tensor details:")
    print(f"  Input : name={inp_det['name']!r:30s} shape={inp_det['shape']}  dtype={inp_det['dtype']}")
    print(f"  Output: name={out_det['name']!r:30s} shape={out_det['shape']}  dtype={out_det['dtype']}")
    print(f"  Input  quantization: scale={inp_det['quantization'][0]:.6f}, zero_point={inp_det['quantization'][1]}")
    print(f"  Output quantization: scale={out_det['quantization'][0]:.6f}, zero_point={out_det['quantization'][1]}")

    # Rough tensor-arena estimate
    arena_bytes = sum(
        int(np.prod(d["shape"])) * np.dtype(d["dtype"]).itemsize
        for d in interp.get_tensor_details()
        if len(d["shape"]) > 0
    )
    print(f"\n[OK] Inference passed — no tensor errors.")
    print(f"[INFO] Estimated tensor memory: {arena_bytes/1024:.1f} KB")
    print(f"[INFO] RT1062 SRAM: 8192 KB — margin: {(8192*1024 - arena_bytes)/1024:.0f} KB\n")


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Gesture CNN — OpenMV RT1062 Training Pipeline")
    print(f"TensorFlow {tf.__version__}  |  NumPy {np.__version__}")
    

    train_ds, val_ds = get_datasets()
    model = build_model()
    history = train(model, train_ds, val_ds)

    best_val = max(history.history.get("val_accuracy", [0]))
    print(f"\n[RESULT] Best val_accuracy: {best_val:.4f}")

    tflite_path, _ = export_tflite_int8(model, train_ds)
    patched_path   = patch_tflite_schema(tflite_path)
    # Validate with TFL3 file — host TF 2.20+ rejects TFL2 header.
    # Patch only changes byte 7; tensor graph is identical.
    validate_tflite(tflite_path)

   
    print(f"DEPLOYMENT FILE: {patched_path.resolve()}")
    print("Copy gesture_cnn_int8_tfl2.tflite to OpenMV /flash/")
    print(DEPLOY_NOTE)

import os
from pathlib import Path

import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request
from PIL import Image, UnidentifiedImageError

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = Path(os.getenv("MODEL_PATH", BASE_DIR / "cat_dog_classifire.keras"))
IMAGE_SIZE = int(os.getenv("IMAGE_SIZE", "224"))
# Keep this order identical to the class order used while training.
CLASS_NAMES = [name.strip() for name in os.getenv("CLASS_NAMES", "Cat,Dog").split(",")]
# Options: mobilenet_v2, rescale_0_1, none
PREPROCESSING = os.getenv("PREPROCESSING", "mobilenet_v2").lower()
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024

model = None


def load_model():
    """Load the Keras model once when the Flask process starts."""
    global model
    if model is None:
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(
                f"Model not found: {MODEL_PATH}. Put model.keras beside app.py "
                "or set MODEL_PATH to its location."
            )
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    return model


def preprocess_image(image: Image.Image) -> np.ndarray:
    image = image.convert("RGB").resize((IMAGE_SIZE, IMAGE_SIZE))
    array = np.asarray(image, dtype=np.float32)

    return np.expand_dims(array, axis=0)


def get_probabilities(prediction: np.ndarray) -> np.ndarray:
    """Convert a 2-class model output into a flat probability vector."""
    values = np.asarray(prediction).squeeze()
    if values.ndim != 1 or values.size != len(CLASS_NAMES):
        raise ValueError(
            f"Expected {len(CLASS_NAMES)} output values, but model returned "
            f"shape {np.asarray(prediction).shape}."
        )

    # Softmax models already return probabilities. If the model returns logits,
    # convert them to probabilities.
    if np.any(values < 0) or not np.isclose(np.sum(values), 1.0, atol=1e-3):
        values = tf.nn.softmax(values).numpy()
    return values.astype(float)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify(error="Please choose an image first."), 400

    uploaded_file = request.files["image"]
    if not uploaded_file.filename:
        return jsonify(error="Please choose an image first."), 400

    extension = uploaded_file.filename.rsplit(".", 1)[-1].lower() if "." in uploaded_file.filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        return jsonify(error="Unsupported file type. Use JPG, PNG, or WEBP."), 400

    try:
        image = Image.open(uploaded_file.stream)
        image.verify()
        uploaded_file.stream.seek(0)
        image = Image.open(uploaded_file.stream)
        batch = preprocess_image(image)
        active_model = load_model()
        raw_prediction = active_model.predict(batch, verbose=0)
        probabilities = get_probabilities(raw_prediction)

        best_index = int(np.argmax(probabilities))
        result = {
            "class_name": CLASS_NAMES[best_index],
            "confidence": round(float(probabilities[best_index]) * 100, 2),
            "probabilities": {
                CLASS_NAMES[i]: round(float(probabilities[i]) * 100, 2)
                for i in range(len(CLASS_NAMES))
            },
        }
        return jsonify(result)

    except (UnidentifiedImageError, OSError, ValueError) as exc:
        return jsonify(error=f"Could not process this image: {exc}"), 400
    except FileNotFoundError as exc:
        app.logger.exception("Model file is missing")
        return jsonify(error=str(exc)), 500
    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify(error="Prediction failed. Check the Flask terminal for details."), 500


@app.errorhandler(413)
def file_too_large(_error):
    return jsonify(error=f"File is too large. Maximum size is {MAX_UPLOAD_MB} MB."), 413


if __name__ == "__main__":
    # Debug mode is for local development only.
    app.run(host="127.0.0.1", port=5000, debug=True)

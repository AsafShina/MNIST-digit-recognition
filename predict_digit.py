import os
import sys

# Set environment variables before importing TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices=0'

# Redirect stderr to devnull before importing anything else
sys.stderr = open(os.devnull, 'w')

import json
import logging
import numpy as np
from PIL import Image

import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

import tensorflow as tf
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Preprocess the image
def preprocess_image(image_path, model_input_shape):
    try:
        img = Image.open(image_path).convert("L")  # Convert to grayscale
        img = img.resize((28, 28))  # Resize to 28x28
        img_array = np.array(img).astype('float32') / 255.0  # Normalize to [0, 1]
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        if len(model_input_shape) == 4:  # Add channel dimension if needed
            img_array = np.expand_dims(img_array, axis=-1)
        return img_array
    except Exception as e:
        # Return error as JSON for PHP
        result = {"error": f"Error during preprocessing: {e}"}
        print(json.dumps(result))
        sys.stdout.flush()
        sys.exit(1)

# Load the trained model and make predictions
try:
    if len(sys.argv) != 2:
        raise ValueError("No image path provided")

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Load the model
    model_path = "MNIST_model.keras"
    model = tf.keras.models.load_model(model_path)

    # Preprocess the input image
    img_array = preprocess_image(image_path, model.input_shape)

    # Predict the digit
    predictions = model.predict(img_array, verbose=0)
    predicted_digit = int(np.argmax(predictions, axis=1)[0])

    # Return the result as JSON
    result = {"predictedDigit": predicted_digit}
    print(json.dumps(result))
    sys.stdout.flush()

except Exception as e:
    # Return the error as JSON for PHP
    result = {"error": str(e)}
    print(json.dumps(result))
    sys.stdout.flush()
    sys.exit(1)

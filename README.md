# MNIST Digit Recognition

This is a web-based application for recognizing handwritten digits using the MNIST dataset. Users can upload an image of a handwritten digit, and the application predicts the digit using a pre-trained model.

can be viwed at http://13.43.187.132/

## Features
- **Upload Images**: Users can upload images in PNG or JPEG format.
- **Digit Recognition**: Predicts a singel handwritten digits using a trained MNIST model.
- **Preview**: Displays the uploaded image before making predictions.

## Project Structure
- `index.html`: Main HTML file for the web interface.
- `styles.css`: CSS file for styling the interface.
- `script.js`: JavaScript file for handling frontend interactions.
- `process.php`: Backend script to handle file uploads and communicate with the Python script.
- `predict_digits.py`: Python script to preprocess images and make predictions using the trained MNIST model.
- `MNIST_model.keras`: Pre-trained ANN model for digit recognition.

## Setup and Installation
### Prerequisites
1. **Local Server**: Use a server like [XAMPP](https://www.apachefriends.org/index.html) or [WAMP](http://www.wampserver.com/).
2. **Python**: Ensure Python 3.7 or later is installed.

### Installation Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/mnist-digit-recognition.git
   cd mnist-digit-recognition
2. Use the following command to install the dependencies:
   ```bash
   pip install -r requirements.txt


# PawVision — Cat vs Dog Classifier

A small single-page website built with Flask, HTML, CSS, and vanilla JavaScript. Upload or drag-and-drop a pet photo, click **Predict**, and view the predicted class, confidence, and both class probabilities.

## Project structure

```text
dog_cat_classifier/
├── app.py
├── model.keras              # add your trained model here (not included)
├── requirements.txt
├── .env.example
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/main.js
```

## 1. Add your model

Copy your trained `model.keras` file into this project folder, next to `app.py`.

The model file is intentionally not included in this source package.

## 2. Create and activate a virtual environment

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> Install a TensorFlow version compatible with your Python version and operating system. If TensorFlow is already installed in your ML environment, you can install only the other requirements there.

## 3. Check the model configuration

The defaults are:

- Input: `224 × 224`, RGB
- Class order: index 0 = `Cat`, index 1 = `Dog`
- Preprocessing: `mobilenet_v2.preprocess_input` (pixel values mapped to approximately `[-1, 1]`)
- Output: two class scores/probabilities

**These settings must match the exact pipeline used to train your model.** If you trained with `image / 255.0`, change preprocessing to `rescale_0_1`. If your model expects raw pixel values, use `none`. If your class order is different, change `CLASS_NAMES`.

Linux / macOS:

```bash
export IMAGE_SIZE=224
export CLASS_NAMES=Cat,Dog
export PREPROCESSING=mobilenet_v2
python app.py
```

Windows PowerShell:

```powershell
$env:IMAGE_SIZE="224"
$env:CLASS_NAMES="Cat,Dog"
$env:PREPROCESSING="mobilenet_v2"
python app.py
```

Or edit the defaults at the top of `app.py`. The `.env.example` file is a reference; it is not automatically loaded.

## 4. Run the website

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## API

`POST /predict`

Send `multipart/form-data` with a file field named `image`.

Example JSON response:

```json
{
  "class_name": "Dog",
  "confidence": 98.5,
  "probabilities": {
    "Cat": 1.5,
    "Dog": 98.5
  }
}
```

## Important notes

- The model is loaded once when the first prediction is made, then reused.
- Uploads are processed in memory; images are not saved to the server.
- Maximum upload size defaults to 10 MB.
- This is a local development server. Do not deploy Flask's debug server publicly.
- The confidence value is the model's output probability, not a guarantee of correctness.

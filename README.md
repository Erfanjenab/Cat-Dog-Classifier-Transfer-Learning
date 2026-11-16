# 🐱🐶 Cat & Dog Image Classifier

A deep learning project that classifies images of cats and dogs using **Transfer Learning** with the **EfficientNetB0** architecture.

The model uses ImageNet-pretrained weights as a frozen feature extractor, combined with a custom classification head to distinguish between two classes.

## 🚀 Project Overview

This project demonstrates how Transfer Learning can be used to build an image classification model with a relatively small dataset.

- **Task:** Binary Image Classification
- **Architecture:** EfficientNetB0
- **Approach:** Transfer Learning (Feature Extraction)
- **Input Size:** 224 × 224 × 3
- **Classes:** Cat & Dog

## 🧠 Model Architecture

The pretrained EfficientNetB0 backbone is used as a frozen feature extractor. A custom classification head is added on top:

```text
EfficientNetB0 (Frozen)
        │
GlobalAveragePooling2D
        │
Dense (64, ReLU)
        │
Dropout (0.5)
        │
Dense (2, Softmax)
```

The backbone retains its ImageNet-pretrained weights, while only the newly added classification layers are trained.

## 📊 Dataset

The dataset was obtained from Kaggle and contains **1,000 images**:

| Class | Images |
|:---|---:|
| 🐱 Cats | 500 |
| 🐶 Dogs | 500 |
| **Total** | **1,000** |

All images were resized to 224 × 224 pixels before being fed into the model.

## ⚙️ Training Configuration

| Parameter | Value |
|:---|:---|
| Optimizer | Adam |
| Loss Function | Categorical Crossentropy |
| Learning Rate | 0.0001 |
| Batch Size | 1 |
| Epochs | 7 |
| Input Shape | (224, 224, 3) |

## 📈 Model Evaluation

The model was evaluated on a test set containing 100 images.

| Metric | Score |
|:---|---:|
| Accuracy | **100%** |
| Precision (Macro) | **1.00** |
| Recall (Macro) | **1.00** |
| F1-Score (Macro) | **1.00** |

Both classes achieved perfect precision, recall, and F1-score on the evaluated test set.

> Note: These results represent performance on the available test set and do not guarantee the same accuracy on unseen real-world images.

## 💻 Hardware

The model was trained using the following hardware:

- **GPU:** NVIDIA RTX 2050 (4GB VRAM)
- **CPU:** Intel Core i5-13420H
- **RAM:** 16GB

## 🛠️ Technologies Used

- Python
- TensorFlow & Keras
- NumPy
- Pandas
- Matplotlib
- Pillow (PIL)
- Scikit-learn
- MLxtend

## 📁 Project Structure

```text
project/
│
├── dataset/
├── Plots/
├── dog_cat_classifier_web/
├── new_pictures/
│
├── cat_dog_model_classifier.keras
├── requirements.txt
└── README.md
```

## ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/Erfanjenab/REPOSITORY_NAME.git
cd REPOSITORY_NAME
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## 🎯 Future Improvements

- Fine-tuning selected EfficientNetB0 layers.
- Experimenting with data augmentation.
- Evaluating the model on a larger and more diverse dataset.
- Improving generalization on real-world images.

---

⭐ If you find this project interesting, consider giving the repository a star!

**Built with ❤️ using TensorFlow and Transfer Learning.**
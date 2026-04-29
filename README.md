# 🍎 AI Fruit & Vegetable Recognition with Calorie Analyzer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://www.djangoproject.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-orange.svg)](https://www.tensorflow.org/)

AN AI application that identifies fruits and vegetables from images and provides real-time nutritional data. This project leverages **Transfer Learning** for high-accuracy computer vision and integrates with a nutrition API for real-time data.

🚀 Key Features
- Deep Learning Classifier: Uses a "MobileNetV2" model trained via transfer learning to identify a wide variety of produce.
- Nutritional Insights: Integration with the **CalorieNinjas API** to provide calories, protein, fats, and fiber content for the identified item.
- Robust Backend: A Django REST API handles image processing and model inference seamlessly.
- Responsive Web UI: A clean interface for users to upload images and view analysis results instantly.

---

## 🛠️ Tech Stack
- Deep Learning: TensorFlow, Keras, MobileNetV2
- Backend: Django, Django REST Framework
- Data Source: CalorieNinjas API
- Frontend: HTML5, CSS3, JavaScript

---

## 📸 Demo
[Project Demo]("C:\Users\Ashwin\Videos\AI Nutrition Analysis video.mp4")

---

## ⚙️ How It Works
1. Model Inference: When a user uploads an image, the pre-trained **MobileNetV2** model extracts features and classifies the image.
2. API Interaction: The predicted label (e.g., "Banana") is sent to the **CalorieNinjas API**.
3. Data Rendering: The nutritional profile is returned and displayed on the dashboard for the user.


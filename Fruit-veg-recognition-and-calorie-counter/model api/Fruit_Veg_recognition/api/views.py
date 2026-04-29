from pathlib import Path

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import tensorflow as tf
from PIL import Image
import numpy as np

class_labels = [
    "apple", "banana", "beetroot", "bell pepper", "cabbage", "capsicum",
    "carrot", "cauliflower", "chilli pepper", "corn", "cucumber", "eggplant", 
    "garlic", "ginger", "grapes", "jalepeno", "kiwi", "lemon", "lettuce", 
    "mango", "onion", "orange", "paprika", "pear", "peas", "pineapple", 
    "pomegranate", "potato", "raddish", "soy beans", "spinach", "sweetcorn", 
    "sweetpotato", "tomato", "turnip", "watermelon"
]

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'fruit&vegetable_model.h5'
model = None


def get_model():
    global model
    if model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f'Model file not found: {MODEL_PATH}')
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    return model


def cors_response(data, status=200):
    response = JsonResponse(data, status=status)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@csrf_exempt
@require_http_methods(['POST', 'OPTIONS'])
def predict_food(request):
    if request.method == 'OPTIONS':
        return cors_response({})

    image_file = request.FILES.get('image')
    if image_file is None:
        return cors_response({'error': 'No image file uploaded.'}, status=400)

    try:
        image = Image.open(image_file).convert('RGB')
        image = image.resize((224, 224))
        image_array = np.array(image, dtype=np.float32) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        predictions = get_model().predict(image_array, verbose=0)
        predicted_class = int(np.argmax(predictions, axis=1)[0])
        predicted_class_name = class_labels[predicted_class]
        return cors_response({'predicted_class': predicted_class_name})
    except Exception as exc:
        return cors_response({'error': str(exc)}, status=400)

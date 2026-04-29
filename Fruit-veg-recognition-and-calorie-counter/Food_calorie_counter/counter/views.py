# from django.shortcuts import render
# import json
# import requests

# # Create your views here.
# def home(request):
#           # for better understanding see python json and requests modules
          

#           if request.method == "POST":
#                     query = request.POST['query'] # Retrieve the query from the POST data   
#                     api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
#                     api_request = requests.get(api_url+query, headers = ({'X-Api-Key': '/sC8HY71YyfJauqkfrxMrw==iVb36DrKfhki81AC'}))
                    

#                     # serialization--> using json.dumps() converting python object into json
#                     # deserialization --> using json.loads() converting json to python obj
#                     try:
#                               api = json.loads(api_request.content)
#                               print(api_request.content)
#                               #print(type(api))
                              

#                     except Exception as e:
#                               api = "oops! There was an error"
#                               print(e)
#                     return render(request,'home.html',{'api':api})

#           else:
#                     return render(request,'home.html',{'query':'Enter a valid query'})




import requests
import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse


LOCAL_NUTRITION = {
    'apple': {'name': 'apple', 'calories': 52, 'carbohydrates_total_g': 14, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.2, 'fiber_g': 2.4, 'potassium_mg': 107, 'protein_g': 0.3, 'sodium_mg': 1, 'sugar_g': 10},
    'banana': {'name': 'banana', 'calories': 89, 'carbohydrates_total_g': 23, 'cholesterol_mg': 0, 'fat_saturated_g': 0.1, 'fat_total_g': 0.3, 'fiber_g': 2.6, 'potassium_mg': 358, 'protein_g': 1.1, 'sodium_mg': 1, 'sugar_g': 12},
    'beetroot': {'name': 'beetroot', 'calories': 43, 'carbohydrates_total_g': 10, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.2, 'fiber_g': 2.8, 'potassium_mg': 325, 'protein_g': 1.6, 'sodium_mg': 78, 'sugar_g': 7},
    'bell pepper': {'name': 'bell pepper', 'calories': 31, 'carbohydrates_total_g': 6, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.3, 'fiber_g': 2.1, 'potassium_mg': 211, 'protein_g': 1, 'sodium_mg': 4, 'sugar_g': 4.2},
    'cabbage': {'name': 'cabbage', 'calories': 25, 'carbohydrates_total_g': 6, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.1, 'fiber_g': 2.5, 'potassium_mg': 170, 'protein_g': 1.3, 'sodium_mg': 18, 'sugar_g': 3.2},
    'capsicum': {'name': 'capsicum', 'calories': 31, 'carbohydrates_total_g': 6, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.3, 'fiber_g': 2.1, 'potassium_mg': 211, 'protein_g': 1, 'sodium_mg': 4, 'sugar_g': 4.2},
    'carrot': {'name': 'carrot', 'calories': 41, 'carbohydrates_total_g': 10, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.2, 'fiber_g': 2.8, 'potassium_mg': 320, 'protein_g': 0.9, 'sodium_mg': 69, 'sugar_g': 4.7},
    'cauliflower': {'name': 'cauliflower', 'calories': 25, 'carbohydrates_total_g': 5, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.3, 'fiber_g': 2, 'potassium_mg': 299, 'protein_g': 1.9, 'sodium_mg': 30, 'sugar_g': 1.9},
    'chilli pepper': {'name': 'chilli pepper', 'calories': 40, 'carbohydrates_total_g': 9, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.4, 'fiber_g': 1.5, 'potassium_mg': 322, 'protein_g': 1.9, 'sodium_mg': 9, 'sugar_g': 5.3},
    'corn': {'name': 'corn', 'calories': 86, 'carbohydrates_total_g': 19, 'cholesterol_mg': 0, 'fat_saturated_g': 0.2, 'fat_total_g': 1.2, 'fiber_g': 2.7, 'potassium_mg': 270, 'protein_g': 3.2, 'sodium_mg': 15, 'sugar_g': 3.2},
    'cucumber': {'name': 'cucumber', 'calories': 15, 'carbohydrates_total_g': 3.6, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.1, 'fiber_g': 0.5, 'potassium_mg': 147, 'protein_g': 0.7, 'sodium_mg': 2, 'sugar_g': 1.7},
    'eggplant': {'name': 'eggplant', 'calories': 25, 'carbohydrates_total_g': 6, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.2, 'fiber_g': 3, 'potassium_mg': 229, 'protein_g': 1, 'sodium_mg': 2, 'sugar_g': 3.5},
    'garlic': {'name': 'garlic', 'calories': 149, 'carbohydrates_total_g': 33, 'cholesterol_mg': 0, 'fat_saturated_g': 0.1, 'fat_total_g': 0.5, 'fiber_g': 2.1, 'potassium_mg': 401, 'protein_g': 6.4, 'sodium_mg': 17, 'sugar_g': 1},
    'ginger': {'name': 'ginger', 'calories': 80, 'carbohydrates_total_g': 18, 'cholesterol_mg': 0, 'fat_saturated_g': 0.2, 'fat_total_g': 0.8, 'fiber_g': 2, 'potassium_mg': 415, 'protein_g': 1.8, 'sodium_mg': 13, 'sugar_g': 1.7},
    'grapes': {'name': 'grapes', 'calories': 69, 'carbohydrates_total_g': 18, 'cholesterol_mg': 0, 'fat_saturated_g': 0.1, 'fat_total_g': 0.2, 'fiber_g': 0.9, 'potassium_mg': 191, 'protein_g': 0.7, 'sodium_mg': 2, 'sugar_g': 15.5},
    'jalepeno': {'name': 'jalapeno', 'calories': 29, 'carbohydrates_total_g': 6.5, 'cholesterol_mg': 0, 'fat_saturated_g': 0.1, 'fat_total_g': 0.4, 'fiber_g': 2.8, 'potassium_mg': 248, 'protein_g': 0.9, 'sodium_mg': 3, 'sugar_g': 4.1},
    'kiwi': {'name': 'kiwi', 'calories': 61, 'carbohydrates_total_g': 15, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.5, 'fiber_g': 3, 'potassium_mg': 312, 'protein_g': 1.1, 'sodium_mg': 3, 'sugar_g': 9},
    'lemon': {'name': 'lemon', 'calories': 29, 'carbohydrates_total_g': 9, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.3, 'fiber_g': 2.8, 'potassium_mg': 138, 'protein_g': 1.1, 'sodium_mg': 2, 'sugar_g': 2.5},
    'lettuce': {'name': 'lettuce', 'calories': 15, 'carbohydrates_total_g': 2.9, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.2, 'fiber_g': 1.3, 'potassium_mg': 194, 'protein_g': 1.4, 'sodium_mg': 28, 'sugar_g': 0.8},
    'mango': {'name': 'mango', 'calories': 60, 'carbohydrates_total_g': 15, 'cholesterol_mg': 0, 'fat_saturated_g': 0.1, 'fat_total_g': 0.4, 'fiber_g': 1.6, 'potassium_mg': 168, 'protein_g': 0.8, 'sodium_mg': 1, 'sugar_g': 13.7},
    'onion': {'name': 'onion', 'calories': 40, 'carbohydrates_total_g': 9, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.1, 'fiber_g': 1.7, 'potassium_mg': 146, 'protein_g': 1.1, 'sodium_mg': 4, 'sugar_g': 4.2},
    'orange': {'name': 'orange', 'calories': 47, 'carbohydrates_total_g': 12, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.1, 'fiber_g': 2.4, 'potassium_mg': 181, 'protein_g': 0.9, 'sodium_mg': 0, 'sugar_g': 9.4},
    'paprika': {'name': 'paprika', 'calories': 282, 'carbohydrates_total_g': 54, 'cholesterol_mg': 0, 'fat_saturated_g': 2.1, 'fat_total_g': 13, 'fiber_g': 35, 'potassium_mg': 2280, 'protein_g': 14, 'sodium_mg': 68, 'sugar_g': 10},
    'pear': {'name': 'pear', 'calories': 57, 'carbohydrates_total_g': 15, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.1, 'fiber_g': 3.1, 'potassium_mg': 116, 'protein_g': 0.4, 'sodium_mg': 1, 'sugar_g': 9.8},
    'peas': {'name': 'peas', 'calories': 81, 'carbohydrates_total_g': 14, 'cholesterol_mg': 0, 'fat_saturated_g': 0.1, 'fat_total_g': 0.4, 'fiber_g': 5.1, 'potassium_mg': 244, 'protein_g': 5.4, 'sodium_mg': 5, 'sugar_g': 5.7},
    'pineapple': {'name': 'pineapple', 'calories': 50, 'carbohydrates_total_g': 13, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.1, 'fiber_g': 1.4, 'potassium_mg': 109, 'protein_g': 0.5, 'sodium_mg': 1, 'sugar_g': 9.9},
    'pomegranate': {'name': 'pomegranate', 'calories': 83, 'carbohydrates_total_g': 19, 'cholesterol_mg': 0, 'fat_saturated_g': 0.1, 'fat_total_g': 1.2, 'fiber_g': 4, 'potassium_mg': 236, 'protein_g': 1.7, 'sodium_mg': 3, 'sugar_g': 13.7},
    'potato': {'name': 'potato', 'calories': 77, 'carbohydrates_total_g': 17, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.1, 'fiber_g': 2.2, 'potassium_mg': 425, 'protein_g': 2, 'sodium_mg': 6, 'sugar_g': 0.8},
    'raddish': {'name': 'radish', 'calories': 16, 'carbohydrates_total_g': 3.4, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.1, 'fiber_g': 1.6, 'potassium_mg': 233, 'protein_g': 0.7, 'sodium_mg': 39, 'sugar_g': 1.9},
    'soy beans': {'name': 'soy beans', 'calories': 446, 'carbohydrates_total_g': 30, 'cholesterol_mg': 0, 'fat_saturated_g': 2.9, 'fat_total_g': 20, 'fiber_g': 9, 'potassium_mg': 1797, 'protein_g': 36, 'sodium_mg': 2, 'sugar_g': 7},
    'spinach': {'name': 'spinach', 'calories': 23, 'carbohydrates_total_g': 3.6, 'cholesterol_mg': 0, 'fat_saturated_g': 0.1, 'fat_total_g': 0.4, 'fiber_g': 2.2, 'potassium_mg': 558, 'protein_g': 2.9, 'sodium_mg': 79, 'sugar_g': 0.4},
    'sweetcorn': {'name': 'sweet corn', 'calories': 86, 'carbohydrates_total_g': 19, 'cholesterol_mg': 0, 'fat_saturated_g': 0.2, 'fat_total_g': 1.2, 'fiber_g': 2.7, 'potassium_mg': 270, 'protein_g': 3.2, 'sodium_mg': 15, 'sugar_g': 3.2},
    'sweetpotato': {'name': 'sweet potato', 'calories': 86, 'carbohydrates_total_g': 20, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.1, 'fiber_g': 3, 'potassium_mg': 337, 'protein_g': 1.6, 'sodium_mg': 55, 'sugar_g': 4.2},
    'tomato': {'name': 'tomato', 'calories': 18, 'carbohydrates_total_g': 3.9, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.2, 'fiber_g': 1.2, 'potassium_mg': 237, 'protein_g': 0.9, 'sodium_mg': 5, 'sugar_g': 2.6},
    'turnip': {'name': 'turnip', 'calories': 28, 'carbohydrates_total_g': 6, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.1, 'fiber_g': 1.8, 'potassium_mg': 191, 'protein_g': 0.9, 'sodium_mg': 67, 'sugar_g': 3.8},
    'watermelon': {'name': 'watermelon', 'calories': 30, 'carbohydrates_total_g': 8, 'cholesterol_mg': 0, 'fat_saturated_g': 0, 'fat_total_g': 0.2, 'fiber_g': 0.4, 'potassium_mg': 112, 'protein_g': 0.6, 'sodium_mg': 1, 'sugar_g': 6.2},
}


def with_activity_minutes(item):
    calories = float(item.get('calories') or 0)
    item['jog_minutes'] = round(calories / 478 * 60)
    item['yoga_minutes'] = round(calories / 195 * 60)
    item['gym_minutes'] = round(calories / 430 * 60)
    item['walk_minutes'] = round(calories / 257 * 60)
    return item


def nutrition_for(query):
    api_url = f'https://api.calorieninjas.com/v1/nutrition?query={query}'
    headers = {'X-Api-Key': '/sC8HY71YyfJauqkfrxMrw==iVb36DrKfhki81AC'}

    try:
        response = requests.get(api_url, headers=headers, timeout=5)
        response.raise_for_status()
        api = response.json()
        if api.get('items'):
            api['items'][0] = with_activity_minutes(api['items'][0])
            return api
    except requests.RequestException:
        pass

    fallback = LOCAL_NUTRITION.get(query.lower())
    if fallback:
        return {'items': [with_activity_minutes(fallback.copy())], 'source': 'local'}
    return {'error': f'No nutrition data found for "{query}".'}


def home(request):
    query = ""
    api = None
    uploaded_image_url = request.POST.get('uploaded_image_url', '')

    if request.method == "POST":
        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_image_url = fs.url(filename)
            request.session['uploaded_image_url'] = uploaded_image_url

        query = request.POST.get('query', '').strip()

    if not query:
        query = request.GET.get('query', '').strip()

    if query:
        api = nutrition_for(query)
    return render(request, 'home.html', {
        'uploaded_image_url': uploaded_image_url,
        'api': api,
        'query': query,
        'model_api_url': os.environ.get('MODEL_API_URL', 'http://127.0.0.1:8010/predict/'),
    })


def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)
        return JsonResponse({'image_url': uploaded_file_url})

    return render(request, 'home.html')


def get_nutrition(request):
    query = request.GET.get('query', '').strip()
    if not query:
        return JsonResponse({'error': 'Missing query parameter.'}, status=400)
    return JsonResponse(nutrition_for(query))

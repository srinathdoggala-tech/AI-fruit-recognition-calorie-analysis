from django.urls import path
from .views import predict_food

urlpatterns = [
    path('predict/', predict_food, name='predict'),
]

from django.urls import path
from .views import convert_view

app_name = 'weconvert'
urlpatterns = [
    path('', convert_view, name='upload'),
]
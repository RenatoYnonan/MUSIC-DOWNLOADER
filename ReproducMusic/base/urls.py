from django.urls import path
from base.views import *


urlpatterns = [
    path('', Index.as_view(), name='index'),
]
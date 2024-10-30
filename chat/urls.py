from django.contrib import admin
from django.urls import path
from chat.views import home,orcamento

urlpatterns = [
    path('', home),
    path('orcamento',orcamento)
]
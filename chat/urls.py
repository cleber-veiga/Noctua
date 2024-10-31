from django.contrib import admin
from django.urls import path
from chat.views import home,orcamento,chatboot

urlpatterns = [
    path('', home),
    path('orcamento/',orcamento),
    path('chat/',chatboot, name='chat_boot')
]
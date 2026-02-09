from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('api/send-message/', views.send_message, name='send_message'),
    path('api/clear-chat/', views.clear_chat, name='clear_chat'),
]

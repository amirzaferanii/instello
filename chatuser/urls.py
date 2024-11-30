from django.urls import path
from . import views

app_name = 'chat_user'

urlpatterns = [
    path('', views.ChatsView.as_view(), name='chats'),
    path('<int:chat_id>', views.ChatView.as_view(), name='chat'),
    path('chat_list/', views.ListChatsView.as_view(), name='chat_list'),
    path('delete/<int:chat_id>', views.DeleteChatView.as_view(), name='delete_chat'),
]
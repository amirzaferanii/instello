from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from Profile.models import Profile
from .models import Chat, Message
from Account.models import User
from django.db.models import Q



class ChatsView(View):
    def get(self, request):
        chats = Chat.objects.filter(Q(user1=request.user) | Q(user2=request.user)).count()
        return render(request, 'chatuser/chats.html', {"chats": chats})


class ListChatsView(View):
    def get(self, request):
        chats = Chat.objects.filter(Q(user1=request.user) | Q(user2=request.user))
        chat_date = []
        for chat in chats:
            last_message = Message.objects.filter(chat=chat).order_by('timestamp').last()
            other_chat = chat.user2 if chat.user1 == request.user else chat.user1
            other_user_profile = Profile.objects.filter(user=other_chat).first()

            chat_date.append({
                'chat': chat,
                'last_message': last_message,
                'other_chat': other_chat,
                'other_user_profile': other_user_profile
            })

        return render(request, 'chatuser/chat_list.html', {'chats': chat_date})



class ChatView(View):
    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, chat_id=chat_id)
        user = chat.user1 if chat.user2 == request.user else chat.user2
        profile = Profile.objects.get(user=user)
        if request.user != chat.user1 and request.user != chat.user2:
            return redirect('chat_user:chat_list')

        messages = chat.messages.order_by('timestamp')
        return render(request, 'chatuser/chat.html', {'chat': chat, 'messages': messages, 'profile': profile})

    def post(self, request, chat_id):
        chat = get_object_or_404(Chat, chat_id=chat_id)
        if request.user != chat.user1 and request.user != chat.user2:
            return redirect('chat_user:chat_list')
        content = request.POST.get('content')
        if content:
            Message.objects.create(chat=chat, sender=request.user, content=content)

        return redirect('chat_user:chat', chat_id=chat_id)



class DeleteChatView(View):
    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, chat_id=chat_id)
        chat.delete()
        return redirect('chat_user:chats')
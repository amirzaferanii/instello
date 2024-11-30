from Profile.models import Profile
from chatuser.models import Chat, Message
from django.db.models import Q

def profile(request):
    if request.user.is_authenticated:
        user = request.user
        user_chats = Chat.objects.filter(Q(user1=user) | Q(user2=user))
        last_chat_id = []
        for item in user_chats:
            all_id = item.chat_id
            last_chat_id.append(all_id)
        last_messages = Message.objects.filter(chat__chat_id__in=last_chat_id).exclude(sender=user).order_by('-timestamp')[:1]
        profile = Profile.objects.get(user=user)
    else:
        profile = None
        last_messages = None
    return {'profile_current': profile, 'last_messages': last_messages}


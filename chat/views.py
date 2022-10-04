from django.shortcuts import render, redirect
from account.models import Collab, Researcher
from .models import ChatNotification, Chat, ChatRoom
from .filters import ChatNotificationFilter
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.safestring import mark_safe
import json
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class Room(LoginRequiredMixin, View):
    def get(self, request, room_name):
        collab = Collab.objects.get(id=room_name)
        if collab.researcher == request.user or request.user in collab.collaborators.all():
            room = ChatRoom.objects.filter(name=room_name).first()
            chats = []
            if room:
                chats = Chat.objects.filter(room=room)
            else:
                room = ChatRoom(name=room_name)
                room.save()
            return render(request, 'chat/room.html', {'room_name': room_name, 'chats':chats})
        else:
            return redirect('collab')

@login_required
def index(request, id):
    collab = Collab.objects.get(id=id)
    room_name = collab.id
    return redirect('room', room_name)

@login_required
def clearEnvelopeUnreads(request):
    try:
        reg = ChatNotification.objects.filter(owner=request.user)[0]
        reg.unreads = 0
        reg.save()
        placeholder = 0
    except:
        placeholder = 0
    reg1 = Researcher.objects.get(username=request.user.username)
    reg1.envelope_unreads = placeholder
    reg1.save()
    return redirect('envelope_notifications')

@login_required
def showChatNotifications(request):
    context = {}
    filtered_envelope_notifications = ChatNotificationFilter(
        request.GET,
        queryset = ChatNotification.objects.filter(owner=request.user)
    )
    context['filtered_envelope_notifications'] = filtered_envelope_notifications
    paginated_filtered_envelope_notifications = Paginator(filtered_envelope_notifications.qs, 100)
    page_number = request.GET.get('page')
    envelope_notifications_page_obj = paginated_filtered_envelope_notifications.get_page(page_number)
    context['envelope_notifications_page_obj'] = envelope_notifications_page_obj
    total_envelope_notifications = filtered_envelope_notifications.qs.count()
    context['total_envelope_notifications'] = total_envelope_notifications

    return render(request, 'chat/envelope_notifications.html', context)

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
        room = ChatRoom.objects.filter(name=room_name).first()
        chats = []
        if room:
            chats = Chat.objects.filter(room=room)
        else:
            room = ChatRoom(name=room_name)
            room.save()
        return render(request, 'chat/room.html', {'room_name': room_name, 'chats':chats})

def lobby(request):
    return render(request, 'chat/lobby.html')

@login_required
def index(request, id):
    collab = Collab.objects.get(id=id)
    room_name = collab.id
    return redirect('room', room_name)

# @login_required
# def room(request, room_name):
#     collab = Collab.objects.get(id=room_name)
#     if collab.researcher != request.user:
#         entry = ChatNotification()
#         entry.owner = collab.researcher
#         entry.sender = request.user
#         entry.collab = collab
#         entry.room = room_name
#         entry.message = "has entered the chatroom for the project: "
#
#         try:
#             old_entry = ChatNotification.objects.filter(owner=collab.researcher)[0]
#             entry.unreads = old_entry.unreads + 1
#             placeholder = old_entry.unreads + 1
#         except:
#             entry.unreads = 1
#             placeholder = 1
#         entry.save()
#
#         reg = Researcher.objects.get(username=collab.researcher.username)
#         reg.envelope_unreads = placeholder
#         reg.save()
#
#         for person in collab.collaborators.all():
#             if person != request.user:
#                 entry = ChatNotification()
#                 entry.owner = person
#                 entry.sender = request.user
#                 entry.collab = collab
#                 entry.room = room_name
#                 entry.message = "has entered the chatroom for the project: "
#
#                 try:
#                     old_entry = ChatNotification.objects.filter(owner=person)[0]
#                     entry.unreads = old_entry.unreads + 1
#                     placeholder = old_entry.unreads + 1
#                 except:
#                     entry.unreads = 1
#                     placeholder = 1
#                 entry.save()
#
#                 reg = Researcher.objects.get(username=person.username)
#                 reg.envelope_unreads = placeholder
#                 reg.save()
#
#     elif collab.researcher == request.user:
#         for person in collab.collaborators.all():
#             entry = ChatNotification()
#             entry.owner = person
#             entry.sender = request.user
#             entry.collab = collab
#             entry.room = room_name
#             entry.message = "has entered the chatroom for the project: "
#
#             try:
#                 old_entry = ChatNotification.objects.filter(owner=person)[0]
#                 entry.unreads = old_entry.unreads + 1
#                 placeholder = old_entry.unreads + 1
#             except:
#                 entry.unreads = 1
#                 placeholder = 1
#             entry.save()
#
#             reg = Researcher.objects.get(username=person.username)
#             reg.envelope_unreads = placeholder
#             reg.save()
#     room = ChatRoom.objects.filter(name=room_name).first()
#     chats = []
#     if room:
#         chats = Chat.objects.filter(room=room)
#     else:
#         room = ChatRoom(name=room_name)
#         room.save()
#
#     return render(request, 'chat/room.html', {
#         'room_name': room_name, 'collab':collab, 'chats':chats})



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

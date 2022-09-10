from django.shortcuts import render
from account.models import Collab, Notification, Researcher

# Create your views here.
def lobby(request):
    return render(request, 'chat/lobby.html')

def index(request, id):
    collab = Collab.objects.get(id=id)
    return render(request, 'chat/index.html', {'collab':collab})

def room(request, id, room_name):
    collab = Collab.objects.get(id=id)

    if collab.researcher != request.user:
        entry = Notification()
        entry.owner = collab.researcher
        entry.sender = request.user
        entry.collab = collab
        entry.room = room_name
        entry.message = "has entered the chatroom. Join the chat by entering the room name: " + room_name + " under the chat section for the collab"

        try:
            old_entry = Notification.objects.filter(owner=collab.researcher)[0]
            entry.unreads = old_entry.unreads + 1
            placeholder = old_entry.unreads + 1
        except:
            entry.unreads = 1
            placeholder = 1
        entry.save()

        reg = Researcher.objects.get(username=collab.researcher.username)
        reg.bell_unreads = placeholder
        reg.save()

    for person in collab.collaborators.all():
        if person != request.user:
            entry = Notification()
            entry.owner = person
            entry.sender = request.user
            entry.collab = collab
            entry.room = room_name
            entry.message = "has entered the chatroom. Join the chat by entering the room name: " + room_name + " under the chat section for the collab"

            try:
                old_entry = Notification.objects.filter(owner=person)[0]
                entry.unreads = old_entry.unreads + 1
                placeholder = old_entry.unreads + 1
            except:
                entry.unreads = 1
                placeholder = 1
            entry.save()

            reg = Researcher.objects.get(username=person.username)
            reg.bell_unreads = placeholder
            reg.save()


    return render(request, 'chat/room.html', {
        'room_name': room_name, 'collab':collab})

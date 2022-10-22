from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoteEditForm, NoteForm
from account.models import Collab
from .models import Note
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .filters import NoteFilter
from django.core.paginator import Paginator

@login_required
def showNotesInitiated(request, id1):
    collab = Collab.objects.get(id=id1)
    if collab.researcher == request.user:
        context = {}
        filtered_notes = NoteFilter(
            request.GET,
            queryset = Note.objects.filter(collab__id=id1)
        )
        context['filtered_notes'] = filtered_notes
        paginated_filtered_notes = Paginator(filtered_notes.qs, 99)
        page_number = request.GET.get('page')
        notes_page_obj = paginated_filtered_notes.get_page(page_number)
        context['notes_page_obj'] = notes_page_obj
        total_notes = filtered_notes.qs.count()
        context['total_notes'] = total_notes
        context['collab'] = collab

        form = NoteForm()
        if request.method == 'POST':
            form = NoteForm(request.POST, request.FILES, None)
            if form.is_valid():
                form.save(commit=False).collab=collab
                form.save(commit=False).user=request.user
                form.save()
                reg = Note.objects.filter(collab=collab)[0]
                reg.serial = reg.id
                reg.save()

                messages.info(request, "The note has been added successfully")
                return redirect('notes_initiated', id1)
            else:
                messages.error(request, "Please review form input fields below")
        context['form'] = form

        return render(request, 'researchnote/notes.html', context)
    elif request.user in collab.collaborators.all():
        context = {}
        filtered_notes = NoteFilter(
            request.GET,
            queryset = Note.objects.filter(collab__id=id1)
        )
        context['filtered_notes'] = filtered_notes
        paginated_filtered_notes = Paginator(filtered_notes.qs, 99)
        page_number = request.GET.get('page')
        notes_page_obj = paginated_filtered_notes.get_page(page_number)
        context['notes_page_obj'] = notes_page_obj
        total_notes = filtered_notes.qs.count()
        context['total_notes'] = total_notes
        context['collab'] = collab

        form = NoteForm()
        if request.method == 'POST':
            form = NoteForm(request.POST, request.FILES, None)
            if form.is_valid():
                form.save(commit=False).collab=collab
                form.save(commit=False).user=request.user
                form.save()
                reg = Note.objects.filter(collab=collab)[0]
                reg.serial = reg.id
                reg.save()

                messages.info(request, "The note has been added successfully")
                return redirect('notes_accepted', id1)
            else:
                messages.error(request, "Please review form input fields below")
        context['form'] = form

        return render(request, 'researchnote/notes.html', context)
    else:
        return redirect('collab')

@login_required
def showNoteInitiated(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    note = Note.objects.get(id=id2)
    if collab.researcher == request.user:

        form = NoteEditForm(instance=note)
        if request.method=='POST':
            form = NoteEditForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                messages.info(request, "The note has been updated successfully")

                return redirect('notes_initiated', id1)

        context = {'collab': collab, 'note':note, 'form':form}

        return render(request, 'researchnote/note_initiated.html', context)
    elif request.user in collab.collaborators.all():

        form = NoteEditForm(instance=note)
        if request.method=='POST':
            form = NoteEditForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                messages.info(request, "The note has been updated successfully")

                return redirect('notes_initiated', id1)

        context = {'collab': collab, 'note':note, 'form':form}

        return render(request, 'researchnote/note_initiated.html', context)
    else:
        return redirect('collab')

@login_required
def deleteNoteInitiated(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    note = Note.objects.get(id=id2)
    if request.user == collab.researcher:
        obj = get_object_or_404(Note, id=id2)
        if request.method =="POST":
            obj.delete()
            messages.info(request, "The note has been deleted successfully")
            return redirect('notes_initiated', id1)
    elif request.user in collab.collaborators.all():
        obj = get_object_or_404(Note, id=id2)
        if request.method =="POST":
            obj.delete()
            messages.info(request, "The note has been deleted successfully")
            return redirect('notes_accepted', id1)
    else:
        return redirect('collab')
    return render(request, 'researchnote/note_confirm_delete.html', {'note':note, 'collab':collab})

@login_required
def pinNote(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    if collab.researcher == request.user:
        note = Note.objects.get(id=id2)
        reg = Note.objects.filter(collab__id=id1)[0]
        serial_new = int(reg.serial) + 1
        serial_old = serial_new - 1
        reg.serial = serial_new
        note.serial = serial_old
        note.is_pinned = True
        reg.save()
        note.save()
        messages.info(request, "The note has been pinned successfully")
        return redirect('notes_initiated', id1)
    elif request.user in collab.collaborators.all():
        note = Note.objects.get(id=id2)
        reg = Note.objects.filter(collab__id=id1)[0]
        serial_new = int(reg.serial) + 1
        serial_old = serial_new - 1
        reg.serial = serial_new
        note.serial = serial_old
        note.is_pinned = True
        reg.save()
        note.save()
        messages.info(request, "The note has been pinned successfully")
        return redirect('notes_accepted', id1)
    else:
        return redirect('collab')

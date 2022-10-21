from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoteEditForm
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

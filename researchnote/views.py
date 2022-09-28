from django.shortcuts import render, redirect, get_object_or_404
# from .forms import CustomRegisterForm, CollabForm, CustomRegisterFormResearcher, FlagForm, StrangerForm, CollabDocForm, DocUpdateForm, TaskForm, TaskEditForm, TaskUpdateForm
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
    else:
        return redirect('collab')

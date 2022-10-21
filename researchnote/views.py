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
        counter = 0
        for person in task.assigned_to.all():
            counter += 1

        form = TaskStatusForm(instance=task)
        if request.method=='POST':
            form = TaskStatusForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                messages.info(request, "The task has been updated successfully")

                return redirect('tasks_initiated', id1)

        form2 = TaskEditForm(instance=task)
        if request.method=='POST':
            form2 = TaskEditForm(request.POST, instance=task)
            if form2.is_valid():
                form2.save()
                messages.info(request, "The task has been updated successfully")

                return redirect('tasks_initiated', id1)

        counter2 = 0
        for each in task.update_text.all():
            counter2 += 1

        context = {'collab': collab, 'counter':counter, 'counter2':counter2, 'task':task, 'form':form, 'form2':form2}

        return render(request, 'account/note_initiated.html', context)
    elif request.user in collab.collaborators.all():
        counter = 0
        for person in task.assigned_to.all():
            counter += 1

        form3 = TextUpdateForm()
        if request.method == 'POST':
            form3 = TextUpdateForm(request.POST, request.FILES, None)
            if form3.is_valid():
                # text = form3.cleaned_data.get('text')
                form3.save(commit=False).creator=request.user
                form3.save()
                reg1 = TextUpdate.objects.filter(creator=request.user)[0]
                reg = Task.objects.get(id=id2)
                reg.update_text.add(reg1)
                reg.save()

                messages.info(request, "The task has been updated successfully")
                return redirect('tasks_accepted', id1)
            else:
                messages.error(request, "Please review form input fields below")

        counter2 = 0
        for each in task.update_text.all():
            counter2 += 1

        context = {'collab': collab, 'counter':counter, 'counter2':counter2, 'task':task, 'form3':form3}

        return render(request, 'researchnote/note_initiated.html', context)
    else:
        return redirect('collab')

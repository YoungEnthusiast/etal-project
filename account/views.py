import json
import urllib.request
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import CustomRegisterForm, CollabForm, CustomRegisterFormResearcher, FlagForm, TaskStatusForm, StrangerForm, CollabDocForm, DocUpdateForm, TaskForm, TaskEditForm, FolderForm, TextUpdateForm
from .models import Collab, Researcher, Notification, Report, CollabDoc, Task, Folder, TextUpdate
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .filters import InitiatedCollabFilter, BellNotificationFilter, CollabDocFilter, TaskFilter, FolderFilter
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from datetime import datetime, date
from django.core.mail import send_mail
from django.contrib.auth import logout
from dateutil.rrule import rrule, DAILY
from subscription.models import Subscription

def join(request):
    form = StrangerForm()
    if request.method == 'POST':
        form = StrangerForm(request.POST or None)
        if form.is_valid():
            unrefined_first_username = form.cleaned_data.get('first_username')
            first_username = unrefined_first_username.lower()
            if "@gmail.com" in first_username or "@yahoo.com" in first_username or "@outlook.com" in first_username or "yahoo.co.uk" in first_username or "@inbox.com" in first_username or "@mail.com" in first_username or "@gmx.com" in first_username or "@icloud.com" in first_username or "@proton.me" in first_username or "protonmail.com" in first_username or "@aol.com" in first_username or "@yandex.com" in first_username:
                messages.info(request, "Please enter an institution email address")
            else:
                form.save()

                try:
                    send_mail(
                        'Create Account',
                        'Please follow the link https://etal.ac/join/' + str(first_username) + ' to create an account',
                        'taoheed.yusuf@etal.ac',
                        [first_username],
                        fail_silently=False,
                        #html_message = render_to_string('home/home1.html')
                    )
                    messages.info(request, "Please check your inbox")
                except:
                    messages.info(request, "Please enter a valid institution email address")
        else:
            return redirect('join')
    return render(request, 'account/join.html', {'form': form})

def create(request, username):
    username = username
    if request.method == "POST":
        form = CustomRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            x = datetime.now().year + datetime.now().month + datetime.now().day + datetime.now().hour + datetime.now().minute + datetime.now().second + 50*datetime.now().microsecond
            form.save(commit=False).username = username
            form.save(commit=False).email = username
            form.save(commit=False).user_Id = x
            try:
                is_exist = Researcher.objects.get(username=username)
                messages.error(request, "A user with the email already exists")
            except:
                form.save()
                messages.info(request, "Registration was successful!")
                return redirect('researcher_board')
        else:
            messages.error(request, "Please review and correct form input fields")
    else:
        form = CustomRegisterForm()
    return render(request, 'account/account.html', {'form': form, 'username':username})

def logoutRequest(request):
    logout(request)
    return redirect('login')

def loginRequest(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}")
                return redirect('researcher_board')
            else:
                messages.info(request, "Either your email address or password is incorrect.")
        else:
            messages.info(request, "Either your email address or password is incorrect.")
    form = AuthenticationForm()
    return render(request = request, template_name = "account/login.html", context={"form":form})

@login_required
def showResearcherBoard(request):
    initiateds = Collab.objects.filter(researcher=request.user, is_locked=True, is_concluded=False).count()
    accepteds = Collab.objects.filter(collaborators=request.user, is_locked=True, is_concluded=False).count()

    all_concludeds = Collab.objects.filter(Q(researcher=request.user) | Q(collaborators=request.user), is_concluded=True)

    scrolls = all_concludeds.count()//5

    d_scrolls = all_concludeds[:scrolls]

    concludeds = 0

    for each in all_concludeds:
        if each.researcher == request.user:
            concludeds += 1
        elif request.user in each.collaborators.all():
            concludeds += 1
    me = Researcher.objects.get(username=request.user.username)

    current_views = me.views

    all_collaborators = Collab.objects.filter(researcher=request.user).order_by('created')
    total_collaborators = 0
    males = 0
    females = 0
    for each in all_collaborators:
        for another in each.collaborators.all():
            me.past_collaborators.add(another)
            total_collaborators += 1
            me.save()

            if another.gender == "Male":
                males += 1
            elif another.gender == "Female":
                females += 1


    created_list = [""]
    initiated_list = [0]
    accepted_list = [0]
    concluded_list = [0]
    all_dates = []

    all_collaborators_initiated = Collab.objects.filter(researcher=request.user, is_locked=True, is_concluded=False).order_by('locked_date')
    initiateds2 = []
    for any in all_collaborators_initiated:
        initiateds2.append(any.locked_date.strftime('%b %Y'))
    all_collaborators_accepted = Collab.objects.filter(collaborators=request.user, is_locked=True, is_concluded=False).order_by('locked_date')
    accepteds2 = []
    for any2 in all_collaborators_accepted:
        accepteds2.append(any2.locked_date.strftime('%b %Y'))

    all_collaborators_concluded = Collab.objects.filter(Q(researcher=request.user) | Q(collaborators=request.user), is_concluded=True).order_by('concluded_date')
    concludeds2 = []
    for any3 in all_collaborators_concluded:
        concludeds2.append(any3.concluded_date.strftime('%b %Y'))

    my_today = datetime.today()
    try:
        min_date = min(all_collaborators_initiated[0].locked_date, all_collaborators_accepted[0].locked_date, all_collaborators_concluded[0].concluded_date)
    except:
        try:
            min_date = min(all_collaborators_initiated[0].locked_date, all_collaborators_concluded[0].concluded_date)
        except:
            try:
                min_date = min(all_collaborators_accepted[0].locked_date, all_collaborators_concluded[0].concluded_date)
            except:
                try:
                    min_date = min(all_collaborators_initiated[0].locked_date, all_collaborators_accepted[0].locked_date)
                except:
                    try:
                        min_date = min(all_collaborators_initiated[0].locked_date)
                    except:
                        try:
                            min_date = min(all_collaborators_accepted[0].locked_date)
                        except:
                            try:
                                min_date = min(all_collaborators_concluded[0].concluded_date)
                            except:
                                min_date = None

    refined_min_date = min_date

    a = refined_min_date
    b = my_today

    for dt in rrule(DAILY, dtstart=a, until=b):
        if dt.strftime('%b %Y') not in all_dates:
            all_dates.append(dt.strftime('%b %Y'))

    for one in all_dates:
        created_list.append(one)
        initiated_list.append(0)
        accepted_list.append(0)
        concluded_list.append(0)
        for one_2 in initiateds2:
            if one != one_2:
                pass
            elif one == one_2:
                current = initiated_list[-1]
                initiated_list.pop()
                current += 1
                initiated_list.append(current)

        for one_3 in accepteds2:
            if one != one_3:
                pass
            elif one == one_3:
                current2 = accepted_list[-1]
                accepted_list.pop()
                current2 += 1
                accepted_list.append(current2)
        for one_4 in concludeds2:
            if one != one_4:
                pass
            elif one == one_4:
                current3 = concluded_list[-1]
                concluded_list.pop()
                current3 += 1
                concluded_list.append(current3)

    followings = 0
    for each2 in me.followings.all():
        followings += 1

    followers = 0
    for each3 in me.followers.all():
        followers += 1

    internal = Collab.objects.filter(researcher=request.user, funding="Institution Internal Funding").count()
    external = Collab.objects.filter(researcher=request.user, funding="External Funding").count()
    total_funding = internal + external

    return render(request, 'account/researcher_board.html', {'initiateds':initiateds, 'males':males,
                    'accepteds':accepteds, 'concludeds':concludeds, 'current_views':current_views,
                    'initiated_list':initiated_list, 'concluded_list':concluded_list, 'females':females,
                    'created_list':created_list, 'accepted_list':accepted_list, 'all_concludeds':all_concludeds,
                    'followings':followings, 'followers':followers, 'total_collaborators':total_collaborators,
                    'internal':internal, 'external':external, 'total_funding':total_funding, 'scrolls':scrolls,
                    'd_scrolls':d_scrolls})

@login_required
def follow(request, user_Id):
    researcher = Researcher.objects.get(user_Id=user_Id)
    me = Researcher.objects.get(username=request.user.username)
    researcher.followers.add(request.user)
    me.followings.add(researcher)
    messages.info(request, "You have followed successfully")

    return redirect('show_user', user_Id)

@login_required
def unFollow(request, user_Id):
    researcher = Researcher.objects.get(user_Id=user_Id)
    me = Researcher.objects.get(username=request.user.username)
    researcher.followers.remove(request.user)
    me.followings.remove(researcher)
    messages.info(request, "You have unfollowed successfully")

    return redirect('show_user', user_Id)

@login_required
def showCollabs(request):
    context = {}
    filtered_all_collabs = InitiatedCollabFilter(
        request.GET,
        queryset = Collab.objects.filter(is_locked=False)
    )
    context['filtered_all_collabs'] = filtered_all_collabs
    paginated_filtered_all_collabs = Paginator(filtered_all_collabs.qs, 9999999)
    page_number = request.GET.get('page')
    all_collabs_page_obj = paginated_filtered_all_collabs.get_page(page_number)
    context['all_collabs_page_obj'] = all_collabs_page_obj
    total_all_collabs = filtered_all_collabs.qs.count()
    context['total_all_collabs'] = total_all_collabs

    return render(request, 'account/all_collabs.html', context)

@login_required
def showFoldersInitiated(request, id1):
    collab = Collab.objects.get(id=id1)
    today = datetime.now()
    if collab.researcher == request.user:
        try:
            reg = Subscription.objects.filter(user=request.user)[0]
            context = {}
            filtered_folders = FolderFilter(
                request.GET,
                queryset = Folder.objects.filter(collab_id=id1, created__lte=reg.subscription_ends)
                )
            context['filtered_folders'] = filtered_folders
            paginated_filtered_folders = Paginator(filtered_folders.qs, 99)
            page_number = request.GET.get('page')
            folders_page_obj = paginated_filtered_folders.get_page(page_number)
            context['folders_page_obj'] = folders_page_obj
            total_folders = filtered_folders.qs.count()
            context['total_folders'] = total_folders
            context['collab'] = collab

            if today <= reg.subscription_ends:
                form = FolderForm()
                if request.method == 'POST':
                    form = FolderForm(request.POST, request.FILES, None)
                    if form.is_valid():
                        form.save(commit=False).created_by=request.user
                        form.save(commit=False).collab=collab
                        form.save()
                        # reg = CollabDoc.objects.filter(shared_by=request.user)[0]
                        # reg.doc_collaborators.add(request.user)
                        # for person in collab.collaborators.all():
                        #     reg.doc_collaborators.add(person)
                        # reg.save()

                        messages.info(request, "The folder has been created successfully")
                        return redirect('folders_initiated', id1)
                    else:
                        messages.error(request, "Please review form input fields below")
                context['form'] = form
                return render(request, 'account/folders.html', context)
            else:
                context ={}
                context['collab'] = collab
                form = FolderForm()
                messages.error(request, "Please subscribe to have access to collab tools")
                return redirect('upgrade')
                context['form'] = form
                return render(request, 'account/folders.html', context)
        except:
            context ={}
            context['collab'] = collab
            form = FolderForm()
            messages.error(request, "Please subscribe to have access to collab tools")
            return redirect('upgrade')
            context['form'] = form
            return render(request, 'account/folders.html', context)

    elif request.user in collab.collaborators.all():
        context = {}
        filtered_folders = FolderFilter(
            request.GET,
            queryset = Folder.objects.filter(collab_id=id1)
        )
        context['filtered_folders'] = filtered_folders
        paginated_filtered_folders = Paginator(filtered_folders.qs, 99)
        page_number = request.GET.get('page')
        folders_page_obj = paginated_filtered_folders.get_page(page_number)
        context['folders_page_obj'] = folders_page_obj
        total_folders = filtered_folders.qs.count()
        context['total_folders'] = total_folders
        context['collab'] = collab



        form = FolderForm()
        if request.method == 'POST':
            form = FolderForm(request.POST, request.FILES, None)
            if form.is_valid():
                form.save(commit=False).created_by=request.user
                form.save(commit=False).collab=collab
                form.save()
                # reg = CollabDoc.objects.filter(shared_by=request.user)[0]
                # reg.doc_collaborators.add(request.user)
                # for person in collab.collaborators.all():
                #     reg.doc_collaborators.add(person)
                # reg.save()

                messages.info(request, "The folder has been created successfully")
                # return redirect('folders_initiated', id1)
            else:
                messages.error(request, "Please review form input fields below")
        context['form'] = form
        return render(request, 'account/folders.html', context)

    else:
        return redirect('collab')

@login_required
def showCollabDocsInitiated(request, id1, id2):
    collab = Collab.objects.get(id=id1)
    folder = Folder.objects.get(id=id2)
    if collab.researcher == request.user:
        context = {}
        filtered_collab_docs = CollabDocFilter(
            request.GET,
            queryset = CollabDoc.objects.filter(collab_id=id1, folder_id=id2)
        )
        context['filtered_collab_docs'] = filtered_collab_docs
        paginated_filtered_collab_docs = Paginator(filtered_collab_docs.qs, 99)
        page_number = request.GET.get('page')
        collab_docs_page_obj = paginated_filtered_collab_docs.get_page(page_number)
        context['collab_docs_page_obj'] = collab_docs_page_obj
        total_collab_docs = filtered_collab_docs.qs.count()
        context['total_collab_docs'] = total_collab_docs
        context['collab'] = collab
        context['folder'] = folder


        if request.method == 'POST':
            # name = request.POST.get("filename")
            myfile = request.FILES.getlist("uploadfiles")
            for f in myfile:
                document = str(f)

                length = len(document)
                sub3 = length-3
                last3 = document[sub3:length+1]
                lower_last3 = last3.lower()

                sub4 = length-4

                before_last4 = document[:sub4]

                if lower_last3=="png" or lower_last3=="jpg" or lower_last3=="peg" or lower_last3=="gif" or lower_last3=="ico":
                    type="Image"
                elif lower_last3=="mp3" or lower_last3=="amr":
                    type="Audio"
                elif lower_last3=="ocx" or lower_last3=="doc":
                    type="Word"
                elif lower_last3=="mp4":
                    type="Video"
                elif lower_last3=="csv":
                    type="CSV"
                elif lower_last3=="lsx":
                    type="Excel"
                elif lower_last3=="pdf":
                    type="PDF"
                elif lower_last3=="svg":
                    type="SVG"
                elif lower_last3=="zip":
                    type="Zip"
                else:
                    type=last3.upper()


                CollabDoc(name=before_last4, document=f, collab=collab, folder=folder, shared_by=request.user, type=type).save()
            messages.info(request, "Uploaded successfully")

        return render(request, 'account/collab_docs.html', context)
    elif request.user in collab.collaborators.all():
        context = {}
        filtered_collab_docs = CollabDocFilter(
            request.GET,
            queryset = CollabDoc.objects.filter(collab_id=id1, folder_id=id2)
        )
        context['filtered_collab_docs'] = filtered_collab_docs
        paginated_filtered_collab_docs = Paginator(filtered_collab_docs.qs, 99)
        page_number = request.GET.get('page')
        collab_docs_page_obj = paginated_filtered_collab_docs.get_page(page_number)
        context['collab_docs_page_obj'] = collab_docs_page_obj
        total_collab_docs = filtered_collab_docs.qs.count()
        context['total_collab_docs'] = total_collab_docs
        context['collab'] = collab
        context['folder'] = folder


        if request.method == 'POST':
            # name = request.POST.get("filename")
            myfile = request.FILES.getlist("uploadfiles")
            for f in myfile:
                document = str(f)

                length = len(document)
                sub3 = length-3
                last3 = document[sub3:length+1]
                lower_last3 = last3.lower()

                sub4 = length-4

                before_last4 = document[:sub4]

                if lower_last3=="png" or lower_last3=="jpg" or lower_last3=="peg" or lower_last3=="gif" or lower_last3=="ico":
                    type="Image"
                elif lower_last3=="mp3" or lower_last3=="amr":
                    type="Audio"
                elif lower_last3=="ocx" or lower_last3=="doc":
                    type="Word"
                elif lower_last3=="mp4":
                    type="Video"
                elif lower_last3=="csv":
                    type="CSV"
                elif lower_last3=="lsx":
                    type="Excel"
                elif lower_last3=="pdf":
                    type="PDF"
                elif lower_last3=="svg":
                    type="SVG"
                elif lower_last3=="zip":
                    type="Zip"
                else:
                    type=last3.upper()


                CollabDoc(name=before_last4, document=f, collab=collab, folder=folder, shared_by=request.user, type=type).save()
            messages.info(request, "Uploaded successfully")

        return render(request, 'account/collab_docs.html', context)
    else:
        return redirect('collab')

def uploadDoc(request, id1, **kwargs):
    collab = Collab.objects.get(id=id1)
    if collab.researcher == request.user:
        form = CollabDocForm()
        if request.method == 'POST':
            form = CollabDocForm(request.POST, request.FILES, None)
            if form.is_valid():
                raw = form.cleaned_data.get('document')
                document = str(raw)

                length = len(document)
                sub3 = length-3
                last3 = document[sub3:length+1]
                lower_last3 = last3.lower()

                if lower_last3=="png" or lower_last3=="jpg" or lower_last3=="peg" or lower_last3=="gif" or lower_last3=="ico":
                    form.save(commit=False).type="Image"
                elif lower_last3=="mp3" or lower_last3=="amr":
                    form.save(commit=False).type="Audio"
                elif lower_last3=="ocx" or lower_last3=="doc":
                    form.save(commit=False).type="Word"
                elif lower_last3=="mp4":
                    form.save(commit=False).type="Video"
                elif lower_last3=="csv":
                    form.save(commit=False).type="CSV"
                elif lower_last3=="lsx":
                    form.save(commit=False).type="Excel"
                elif lower_last3=="pdf":
                    form.save(commit=False).type="PDF"
                elif lower_last3=="svg":
                    form.save(commit=False).type="SVG"
                elif lower_last3=="zip":
                    form.save(commit=False).type="Zip"
                else:
                    form.save(commit=False).type=last3.upper()
                form.save(commit=False).shared_by=request.user
                form.save(commit=False).collab=collab
                form.save()
                # reg = CollabDoc.objects.filter(shared_by=request.user)[0]
                # reg.doc_collaborators.add(request.user)
                # for person in collab.collaborators.all():
                #     reg.doc_collaborators.add(person)
                # reg.save()

                messages.info(request, "The document has been uploaded successfully")
                return redirect('collab_docs_initiated', id1)
            else:
                messages.error(request, "Please review form input fields below")
        return render(request, 'account/upload_doc.html', {'form':form, 'collab':collab})


    elif request.user in collab.collaborators.all():
        form = CollabDocForm()
        if request.method == 'POST':
            form = CollabDocForm(request.POST, request.FILES, None)
            if form.is_valid():
                raw = form.cleaned_data.get('document')
                document = str(raw)

                length = len(document)
                sub3 = length-3
                last3 = document[sub3:length+1]
                lower_last3 = last3.lower()

                if lower_last3=="png" or lower_last3=="jpg" or lower_last3=="peg" or lower_last3=="gif" or lower_last3=="ico":
                    form.save(commit=False).type="Image"
                elif lower_last3=="mp3" or lower_last3=="amr":
                    form.save(commit=False).type="Audio"
                elif lower_last3=="ocx" or lower_last3=="doc":
                    form.save(commit=False).type="Word"
                elif lower_last3=="mp4":
                    form.save(commit=False).type="Video"
                elif lower_last3=="csv":
                    form.save(commit=False).type="CSV"
                elif lower_last3=="lsx":
                    form.save(commit=False).type="Excel"
                elif lower_last3=="pdf":
                    form.save(commit=False).type="PDF"
                elif lower_last3=="svg":
                    form.save(commit=False).type="SVG"
                elif lower_last3=="zip":
                    form.save(commit=False).type="Zip"
                else:
                    form.save(commit=False).type=last3.upper()
                form.save(commit=False).shared_by=request.user
                form.save(commit=False).collab=collab
                form.save()
                # reg = CollabDoc.objects.filter(shared_by=request.user)[0]
                # reg.doc_collaborators.add(request.user)
                # for person in collab.collaborators.all():
                #     reg.doc_collaborators.add(person)
                # reg.save()

                messages.info(request, "The document has been uploaded successfully")
                return redirect('collab_docs_accepted', id1)
            else:
                messages.error(request, "Please review form input fields below")
        return render(request, 'account/upload_doc.html', {'form':form, 'collab':collab})

    else:
        return redirect('collab')

@login_required
def showTasksInitiated(request, id1):
    collab = Collab.objects.get(id=id1)
    if collab.researcher == request.user:
        context = {}
        filtered_tasks = TaskFilter(
            request.GET,
            queryset = Task.objects.filter(collab__id=id1, status="Ongoing")
        )
        context['filtered_tasks'] = filtered_tasks
        paginated_filtered_tasks = Paginator(filtered_tasks.qs, 99)
        page_number = request.GET.get('page')
        tasks_page_obj = paginated_filtered_tasks.get_page(page_number)
        context['tasks_page_obj'] = tasks_page_obj
        total_tasks = filtered_tasks.qs.count()
        context['total_tasks'] = total_tasks

        #Completed
        filtered_tasks_completed = TaskFilter(
            request.GET,
            queryset = Task.objects.filter(collab__id=id1, status="Completed")
        )
        context['filtered_tasks_completed'] = filtered_tasks_completed
        paginated_filtered_tasks_completed = Paginator(filtered_tasks_completed.qs, 99)
        page_number = request.GET.get('page')
        tasks_completed_page_obj = paginated_filtered_tasks_completed.get_page(page_number)
        context['tasks_completed_page_obj'] = tasks_completed_page_obj
        total_tasks_completed = filtered_tasks_completed.qs.count()
        context['total_tasks_completed'] = total_tasks_completed

        #Stopped
        filtered_tasks_stopped = TaskFilter(
            request.GET,
            queryset = Task.objects.filter(collab__id=id1, status="Stopped")
        )
        context['filtered_tasks_stopped'] = filtered_tasks_stopped
        paginated_filtered_tasks_stopped = Paginator(filtered_tasks_stopped.qs, 99)
        page_number = request.GET.get('page')
        tasks_stopped_page_obj = paginated_filtered_tasks_stopped.get_page(page_number)
        context['tasks_stopped_page_obj'] = tasks_stopped_page_obj
        total_tasks_stopped = filtered_tasks_stopped.qs.count()
        context['total_tasks_stopped'] = total_tasks_stopped

        context['collab'] = collab

        those0 = collab.collaborators.all()

        form = TaskForm(those0)
        if request.method == 'POST':
            form = TaskForm(those0, request.POST, request.FILES, None)
            if form.is_valid():
                form.save(commit=False).collab=collab
                form.save(commit=False).poster=request.user
                form.save()
                reg = Task.objects.filter(collab=collab)[0]
                reg.serial = reg.id
                reg.save()

                messages.info(request, "The task has been added successfully")
                return redirect('tasks_initiated', id1)
            else:
                messages.error(request, "Please review form input fields below")
        context['form'] = form

        return render(request, 'account/tasks.html', context)
    else:
        return redirect('collab')

@login_required
def showTasksAccepted(request, id1):
    collab = Collab.objects.get(id=id1)
    if request.user in collab.collaborators.all():
        context = {}
        filtered_tasks = TaskFilter(
            request.GET,
            queryset = Task.objects.filter(collab__id=id1, status="Ongoing")
        )
        context['filtered_tasks'] = filtered_tasks
        paginated_filtered_tasks = Paginator(filtered_tasks.qs, 99)
        page_number = request.GET.get('page')
        tasks_page_obj = paginated_filtered_tasks.get_page(page_number)
        context['tasks_page_obj'] = tasks_page_obj
        total_tasks = filtered_tasks.qs.count()
        context['total_tasks'] = total_tasks

        #Completed
        filtered_tasks_completed = TaskFilter(
            request.GET,
            queryset = Task.objects.filter(collab__id=id1, status="Completed")
        )
        context['filtered_tasks_completed'] = filtered_tasks_completed
        paginated_filtered_tasks_completed = Paginator(filtered_tasks_completed.qs, 99)
        page_number = request.GET.get('page')
        tasks_completed_page_obj = paginated_filtered_tasks_completed.get_page(page_number)
        context['tasks_completed_page_obj'] = tasks_completed_page_obj
        total_tasks_completed = filtered_tasks_completed.qs.count()
        context['total_tasks_completed'] = total_tasks_completed

        #Stopped
        filtered_tasks_stopped = TaskFilter(
            request.GET,
            queryset = Task.objects.filter(collab__id=id1, status="Stopped")
        )
        context['filtered_tasks_stopped'] = filtered_tasks_stopped
        paginated_filtered_tasks_stopped = Paginator(filtered_tasks_stopped.qs, 99)
        page_number = request.GET.get('page')
        tasks_stopped_page_obj = paginated_filtered_tasks_stopped.get_page(page_number)
        context['tasks_stopped_page_obj'] = tasks_stopped_page_obj
        total_tasks_stopped = filtered_tasks_stopped.qs.count()
        context['total_tasks_stopped'] = total_tasks_stopped

        context['collab'] = collab

        return render(request, 'account/tasks.html', context)
    else:
        return redirect('collab')

@login_required
def showCollabDocsAccepted(request, id1):
    collab = Collab.objects.get(id=id1)
    if request.user in collab.collaborators.all():
        context = {}
        filtered_collab_docs = CollabDocFilter(
            request.GET,
            queryset = CollabDoc.objects.filter(collab__id=id1)
        )
        context['filtered_collab_docs'] = filtered_collab_docs
        paginated_filtered_collab_docs = Paginator(filtered_collab_docs.qs, 99)
        page_number = request.GET.get('page')
        collab_docs_page_obj = paginated_filtered_collab_docs.get_page(page_number)
        context['collab_docs_page_obj'] = collab_docs_page_obj
        total_collab_docs = filtered_collab_docs.qs.count()
        context['total_collab_docs'] = total_collab_docs
        context['collab'] = collab

        return render(request, 'account/collab_docs.html', context)
    else:
        return redirect('collab')

@login_required
def createCollab(request):
    form = CollabForm(request=request)
    if request.method == 'POST':
        form = CollabForm(request.POST, request.FILES, None, request=request)
        if form.is_valid():
            form.save(commit=False).researcher=request.user
            form.save()
            messages.info(request, "The collab has been created successfully")
            return redirect('collab')
        else:
            messages.error(request, "Please review form input fields below")
    return render(request, 'account/create_collab.html', {'form':form})

@login_required
def showResearcherProfile(request, **kwargs):
    me = Researcher.objects.get(username=request.user.username)
    followings = 0
    for each2 in me.followings.all():
        followings += 1

    followers = 0
    for each3 in me.followers.all():
        followers += 1
    if request.method == "POST":
        form = CustomRegisterFormResearcher(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            form.save(commit=False).email = email
            form.save()
            messages.info(request, "Your profile has been modified successfully")
            return redirect('researcher_profile')
        else:
            messages.error(request, "Error: Please review form input fields below")
    else:
        form = CustomRegisterFormResearcher(instance=request.user)

    return render(request, 'account/researcher_profile.html', {'form': form, 'followers':followers, 'followings':followings})

@login_required
def researcherChangePassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            user = request.user
            name = user.first_name
            email = user.email
            send_mail(
                'Password Changed!',
                'Dear ' + str(name) + ', your password has just been changed. If this activity was not carried out by you, please reply to this email',
                'admin@qwikgas.ai',
                [email],
                fail_silently=False,
                # html_message = render_to_string('users/change_password_email.html', {'name': str(name)})
            )
            messages.info(request, "Your password has been changed successfully")
            return redirect('researcher_profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'account/researcher_change_password.html', {'form': form})

@login_required
def showUser(request, user_Id, **kwargs):
    researcher = Researcher.objects.get(user_Id=user_Id)

    current_views = researcher.views
    current_views += 1
    researcher.views = current_views
    researcher.save()

    followings = 0
    try:
        for each in researcher.followings.all():
            followings += 1
    except:
        pass

    followers = 0
    try:
        for each2 in researcher.followers.all():
            followers += 1
    except:
        pass

    all_collaborators = Collab.objects.filter(researcher=researcher).order_by('created')
    total_collaborators = 0
    males = 0
    females = 0
    for each in all_collaborators:
        for another in each.collaborators.all():
            total_collaborators += 1

            if another.gender == "Male":
                males += 1
            elif another.gender == "Female":
                females += 1

    all_concludeds = Collab.objects.filter(Q(researcher=researcher) | Q(collaborators=researcher), is_concluded=True)

    scrolls = all_concludeds.count()//5

    d_scrolls = all_concludeds[:scrolls]

    internal = Collab.objects.filter(researcher=researcher, funding="Institution Internal Funding").count()
    external = Collab.objects.filter(researcher=researcher, funding="External Funding").count()
    total_funding = internal + external

    context = {'researcher': researcher, 'followings': followings, 'followers':followers, 'total_collaborators':total_collaborators,
                'males':males, 'females':females, 'internal':internal, 'external':external, 'total_funding':total_funding, 'scrolls':scrolls,
                'd_scrolls':d_scrolls, 'all_concludeds':all_concludeds}
    return render(request, 'account/user_profile.html', context)

@login_required
def showCollab(request, id, **kwargs):
    collab = Collab.objects.get(id=id)
    form = FlagForm()
    if request.method == 'POST':
        form = FlagForm(request.POST, request.FILES, None)
        if form.is_valid():
            form.save(commit=False).complainer=request.user
            form.save(commit=False).collab=collab
            form.save(commit=False).is_flagged=True
            form.save()
            messages.info(request, "Your flagging reason has been sent for review")
            return redirect('collab')
        else:
            messages.error(request, "Please review form input field")

    context = {'collab': collab, 'form': form}
    return render(request, 'account/collab.html', context)

@login_required
def updateCollab(request, id):
    collab = Collab.objects.get(id=id)
    if collab.researcher == request.user:
        form = CollabForm(instance=collab, request=request)
        if request.method=='POST':
            form = CollabForm(request.POST, instance=collab, request=request)
            if form.is_valid():
                form.save()
                messages.info(request, "The collab has been updated successfully")
                return redirect('collab')
    else:
        messages.info(request, "You are not authorised")
        return redirect('collab')

    return render(request, 'account/update_collab.html', {'form': form, 'collab':collab})

@login_required
def updateFolderInitiated(request, id1, id2):
    collab = Collab.objects.get(id=id1)
    folder = Folder.objects.get(id=id2)
    if folder.created_by == request.user:
        form = FolderForm(instance=folder)
        if request.method=='POST':
            form = FolderForm(request.POST, instance=folder)
            if form.is_valid():
                form.save()
                messages.info(request, "The folder has been updated successfully")
                return redirect('folders_initiated', id1)
    else:
        return redirect('collab')

    return render(request, 'account/update_folder.html', {'form': form, 'collab':collab})

def deleteFolderInitiated(request, id1, id2):
    collab = Collab.objects.get(id=id1)
    folder = Folder.objects.get(id=id2)
    obj = get_object_or_404(Folder, id=id2)
    if request.method =="POST":
        obj.delete()
        messages.info(request, "The folder has been deleted successfully")
        return redirect('folders_initiated', id1)
    return render(request, 'account/folder_confirm_delete_initiated.html', {'collab':collab, 'folder':folder})

@login_required
def deleteCollab(request, id):
    collab = Collab.objects.get(id=id)
    obj = get_object_or_404(Collab, id=id)
    if request.method =="POST":
        obj.delete()
        messages.info(request, "The collab has been deleted successfully")
        return redirect('collab')
    return render(request, 'account/folder_confirm_delete_initiated.html', {'collab':collab})

# @login_required
# def deleteDoc(request, id):
#     doc = CollabDoc.objects.get(id=id)
#     obj = get_object_or_404(CollabDoc, id=id)
#     if request.method =="POST":
#         obj.delete()
#         messages.info(request, "The document has been deleted successfully")
#         return redirect('collab_docs')
#     return render(request, 'account/doc_confirm_delete.html', {'doc':doc})

@login_required
def deleteAllDocsInitiated(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    folder = Folder.objects.get(id=id2)
    if collab.researcher == request.user:
        docs = CollabDoc.objects.filter(is_selected=request.user, shared_by=request.user, collab=collab)
        if docs.count() >= 1:
            if request.method =="POST":
                for each in docs:
                    each.delete()
                messages.info(request, "Deleted successfully")
                return redirect('collab_docs_initiated', id1, id2)
        else:
            return redirect('collab_docs_initiated', id1, id2)

        return render(request, 'account/docs_confirm_delete_initiated.html', {'docs':docs, 'folder':folder, 'collab':collab})
    if request.user in collab.collaborators.all():
        docs = CollabDoc.objects.filter(is_selected=request.user, shared_by=request.user, collab=collab)
        if docs.count() >= 1:
            if request.method =="POST":
                for each in docs:
                    each.delete()
                messages.info(request, "Deleted successfully")
                return redirect('collab_docs_accepted', id1, id2)
        else:
            return redirect('collab_docs_accepted', id1, id2)

        return render(request, 'account/docs_confirm_delete_initiated.html', {'docs':docs, 'folder':folder, 'collab':collab})
    else:
        return redirect('collab')

@login_required
def deleteAllDocsAccepted(request, id1, **kwargs):
    collab = Collab.objects.get(id=id1)
    if request.user in collab.collaborators.all():
        docs = CollabDoc.objects.filter(is_selected=request.user, shared_by=request.user, collab=collab)
        if docs.count() >= 1:
            if request.method =="POST":
                for each in docs:
                    each.delete()
                messages.info(request, "Deleted successfully")
                return redirect('collab_docs_accepted', id1)
        else:
            return redirect('collab_docs_accepted', id1)

        return render(request, 'account/docs_confirm_delete_accepted.html', {'docs':docs, 'collab':collab})
    else:
        return redirect('collab')

@login_required
def uploadDoc(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    folder = Folder.objects.get(id=id2)
    if collab.researcher == request.user:
        form = CollabDocForm()
        if request.method == 'POST':
            form = CollabDocForm(request.POST, request.FILES, None)
            if form.is_valid():
                raw = form.cleaned_data.get('document')
                document = str(raw)

                length = len(document)
                sub3 = length-3
                last3 = document[sub3:length+1]
                lower_last3 = last3.lower()

                if lower_last3=="png" or lower_last3=="jpg" or lower_last3=="peg" or lower_last3=="gif" or lower_last3=="ico":
                    form.save(commit=False).type="Image"
                elif lower_last3=="mp3" or lower_last3=="amr":
                    form.save(commit=False).type="Audio"
                elif lower_last3=="ocx" or lower_last3=="doc":
                    form.save(commit=False).type="Word"
                elif lower_last3=="mp4":
                    form.save(commit=False).type="Video"
                elif lower_last3=="csv":
                    form.save(commit=False).type="CSV"
                elif lower_last3=="lsx":
                    form.save(commit=False).type="Excel"
                elif lower_last3=="pdf":
                    form.save(commit=False).type="PDF"
                elif lower_last3=="svg":
                    form.save(commit=False).type="SVG"
                elif lower_last3=="zip":
                    form.save(commit=False).type="Zip"
                else:
                    form.save(commit=False).type=last3.upper()
                form.save(commit=False).shared_by=request.user
                form.save(commit=False).collab=collab
                form.save()
                # reg = CollabDoc.objects.filter(shared_by=request.user)[0]
                # reg.doc_collaborators.add(request.user)
                # for person in collab.collaborators.all():
                #     reg.doc_collaborators.add(person)
                # reg.save()

                messages.info(request, "The document has been uploaded successfully")
                return redirect('collab_docs_initiated', id1, id2)
            else:
                messages.error(request, "Please review form input fields below")
        return render(request, 'account/upload_doc.html', {'form':form, 'collab':collab})


    elif request.user in collab.collaborators.all():
        form = CollabDocForm()
        if request.method == 'POST':
            form = CollabDocForm(request.POST, request.FILES, None)
            if form.is_valid():
                raw = form.cleaned_data.get('document')
                document = str(raw)

                length = len(document)
                sub3 = length-3
                last3 = document[sub3:length+1]
                lower_last3 = last3.lower()

                if lower_last3=="png" or lower_last3=="jpg" or lower_last3=="peg" or lower_last3=="gif" or lower_last3=="ico":
                    form.save(commit=False).type="Image"
                elif lower_last3=="mp3" or lower_last3=="amr":
                    form.save(commit=False).type="Audio"
                elif lower_last3=="ocx" or lower_last3=="doc":
                    form.save(commit=False).type="Word"
                elif lower_last3=="mp4":
                    form.save(commit=False).type="Video"
                elif lower_last3=="csv":
                    form.save(commit=False).type="CSV"
                elif lower_last3=="lsx":
                    form.save(commit=False).type="Excel"
                elif lower_last3=="pdf":
                    form.save(commit=False).type="PDF"
                elif lower_last3=="svg":
                    form.save(commit=False).type="SVG"
                elif lower_last3=="zip":
                    form.save(commit=False).type="Zip"
                else:
                    form.save(commit=False).type=last3.upper()
                form.save(commit=False).shared_by=request.user
                form.save(commit=False).collab=collab
                form.save()
                # reg = CollabDoc.objects.filter(shared_by=request.user)[0]
                # reg.doc_collaborators.add(request.user)
                # for person in collab.collaborators.all():
                #     reg.doc_collaborators.add(person)
                # reg.save()

                messages.info(request, "The document has been uploaded successfully")
                return redirect('collab_docs_accepted', id1, id2)
            else:
                messages.error(request, "Please review form input fields below")
        return render(request, 'account/upload_doc.html', {'form':form, 'collab':collab})

    else:
        return redirect('collab')

@login_required
def addTask(request, id1, **kwargs):
    collab = Collab.objects.get(id=id1)
    if collab.researcher == request.user:
        form = TaskForm()
        if request.method == 'POST':
            form = TaskForm(request.POST, request.FILES, None)
            if form.is_valid():
                form.save(commit=False).collab=collab
                form.save()
                reg = Task.objects.filter(collab=collab)[0]
                reg.serial = reg.id
                reg.save()

                messages.info(request, "The task has been added successfully")
                return redirect('tasks_initiated', id1)
            else:
                messages.error(request, "Please review form input fields below")
        return render(request, 'account/add_task.html', {'form':form, 'collab':collab})
    elif request.user in collab.collaborators.all():
        form = TaskForm()
        if request.method == 'POST':
            form = TaskForm(request.POST, request.FILES, None)
            if form.is_valid():
                form.save(commit=False).collab=collab
                form.save()
                reg = Task.objects.all()[0]
                reg.serial = reg.id
                reg.save()

                messages.info(request, "The task has been added successfully")
                return redirect('tasks_accepted', id1)
            else:
                messages.error(request, "Please review form input fields below")
        return render(request, 'account/add_task.html', {'form':form, 'collab':collab})

    else:
        return redirect('collab')


@login_required
def selectDocInitiated(request, id1, id2, id3, **kwargs):
    collab = Collab.objects.get(id=id1)
    folder = Folder.objects.get(id=id2)
    if collab.researcher == request.user:
        doc = CollabDoc.objects.get(id=id3)
        doc.is_selected.add(request.user)
        doc.save()
        return redirect('collab_docs_initiated', id1, id2)
    elif request.user in collab.collaborators.all():
        doc = CollabDoc.objects.get(id=id3)
        doc.is_selected.add(request.user)
        doc.save()
        return redirect('collab_docs_accepted', id1, id2)
    else:
        return redirect('collab')

# @login_required
# def selectDocAccepted(request, id1, id2, **kwargs):
#     collab = Collab.objects.get(id=id1)
#     if request.user in collab.collaborators.all():
#         doc = CollabDoc.objects.get(id=id2)
#         doc.is_selected.add(request.user)
#         doc.save()
#         return redirect('collab_docs_accepted', id1)
#     else:
#         return redirect('collab')

@login_required
def deselectDocInitiated(request, id1, id2, id3, **kwargs):
    collab = Collab.objects.get(id=id1)
    folder = Folder.objects.get(id=id2)
    if collab.researcher == request.user:
        doc = CollabDoc.objects.get(id=id3)
        doc.is_selected.remove(request.user)
        doc.save()
        return redirect('collab_docs_initiated', id1, id2)
    elif request.user in collab.collaborators.all():
        doc = CollabDoc.objects.get(id=id3)
        doc.is_selected.remove(request.user)
        doc.save()
        return redirect('collab_docs_accepted', id1, id2)
    else:
        return redirect('collab')

@login_required
def deselectDocAccepted(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    if request.user in collab.collaborators.all():
        doc = CollabDoc.objects.get(id=id2)
        doc.is_selected.remove(request.user)
        doc.save()
        return redirect('collab_docs_accepted', id1)
    else:
        return redirect('collab')

@login_required
def updateDocInitiated(request, id1, id2, id3, **kwargs):
    collab = Collab.objects.get(id=id1)
    folder = Folder.objects.get(id=id2)
    if collab.researcher == request.user:
        doc = CollabDoc.objects.get(id=id3)
        form = DocUpdateForm(instance=doc)
        if request.method=='POST':
            form = DocUpdateForm(request.POST, instance=doc)
            if form.is_valid():
                if doc.shared_by==request.user:
                    form.save()
                    messages.info(request, "The document has been renamed successfully")
                else:
                    messages.info(request, "You are not authorised to rename the document")

                return redirect('collab_docs_initiated', id1, id2)
        return render(request, 'account/update_doc.html', {'form': form, 'doc':doc, 'folder':folder, 'collab':collab})
    elif request.user in collab.collaborators.all():
        doc = CollabDoc.objects.get(id=id3)
        form = DocUpdateForm(instance=doc)
        if request.method=='POST':
            form = DocUpdateForm(request.POST, instance=doc)
            if form.is_valid():
                if doc.shared_by==request.user:
                    form.save()
                    messages.info(request, "The document has been renamed successfully")
                else:
                    messages.info(request, "You are not authorised to rename the document")

                return redirect('collab_docs_accepted', id1, id2)
        return render(request, 'account/update_doc.html', {'form': form, 'doc':doc, 'folder':folder, 'collab':collab})
    else:
        return redirect('collab')

@login_required
def editTaskInitiated(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    if collab.researcher == request.user:
        task = Task.objects.get(id=id2)
        form = TaskEditForm(instance=task)
        if request.method=='POST':
            form = TaskEditForm(request.POST, instance=task)
            if form.is_valid():

                form.save()
                messages.info(request, "The task has been edited successfully")
                return redirect('tasks_initiated', id1)
        return render(request, 'account/edit_task.html', {'form': form, 'task':task, 'collab':collab})
    else:
        return redirect('collab')

@login_required
def updateTaskAccepted(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    if request.user in collab.collaborators.all():
        task = Task.objects.get(id=id2)
        form = TextUpdateForm(instance=task)
        if request.method=='POST':
            form = TextUpdateForm(request.POST, instance=task)
            if form.is_valid():
                for person in task.text_editor.all():
                    task.text_editor.remove(person)
                task.text_editor.add(request.user)
                form.save(commit=False).updated_date = datetime.now()
                form.save()
                messages.info(request, "The task has been updated successfully")

                return redirect('tasks_accepted', id1)
        return render(request, 'account/update_task.html', {'form': form, 'task':task, 'collab':collab})
    else:
        return redirect('collab')

@login_required
def pinTask(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    if collab.researcher == request.user:
        task = Task.objects.get(id=id2)
        reg = Task.objects.filter(collab__id=id1)[0]
        serial_new = int(reg.serial) + 1
        serial_old = serial_new - 1
        reg.serial = serial_new
        task.serial = serial_old
        task.is_pinned = True
        reg.save()
        task.save()
        messages.info(request, "The task has been pinned successfully")
        return redirect('tasks_initiated', id1)
    elif request.user in collab.collaborators.all():
        task = Task.objects.get(id=id2)
        reg = Task.objects.filter(collab__id=id1)[0]
        serial_new = int(reg.serial) + 1
        serial_old = serial_new - 1
        reg.serial = serial_new
        task.serial = serial_old
        task.is_pinned = True
        reg.save()
        task.save()
        messages.info(request, "The task has been pinned successfully")
        return redirect('tasks_accepted', id1)
    else:
        return redirect('collab')

@login_required
def deleteTaskInitiated(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    task = Task.objects.get(id=id2)
    obj = get_object_or_404(Task, id=id2)
    if request.method =="POST":
        obj.delete()
        messages.info(request, "The task has been deleted successfully")
        return redirect('tasks_initiated', id1)
    return render(request, 'account/task_confirm_delete.html', {'task':task, 'collab':collab})

@login_required
def showCollabInitiated(request, id1, **kwargs):
    collab = Collab.objects.get(id=id1)
    if collab.researcher == request.user:
        counter = 0
        for person in collab.collaborators.all():
            counter += 1

        context = {'collab': collab, 'counter':counter}

        return render(request, 'account/collab_initiated.html', context)
    else:
        return redirect('collab')

@login_required
def showTaskInitiated(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    task = Task.objects.get(id=id2)
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

        return render(request, 'account/task_initiated.html', context)
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

        return render(request, 'account/task_initiated.html', context)
    else:
        return redirect('collab')

@login_required
def showCollabAccepted(request, id, **kwargs):
    collab = Collab.objects.get(id=id)
    if request.user in collab.collaborators.all():
        counter = 0
        for person in collab.collaborators.all():
            counter += 1

        context = {'collab': collab, 'counter':counter}
        return render(request, 'account/collab_accepted.html', context)
    else:
        return redirect('collab')

@login_required
def interestCollab(request, id):
    collab = Collab.objects.get(id=id)
    collab.interested_people.add(request.user)
    messages.info(request, "Your interest has been notified to the researcher")
    collab.save()

    entry = Notification()
    entry.owner = collab.researcher
    entry.sender = request.user
    entry.collab = collab
    entry.message = "showed interest on"
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
    return redirect('collab')

@login_required
def lockCollab(request, id):
    collab = Collab.objects.get(id=id)
    if collab.researcher == request.user:
        collab.is_locked = True
        collab.locked_date = datetime.now()
        collab.save()
        messages.info(request, "The collab has been locked sucessfully")
        return redirect('collab')
    else:
        return redirect('collab')

@login_required
def concludeCollab(request, id):
    collab = Collab.objects.get(id=id)
    if collab.researcher == request.user:
        collab.is_concluded = True
        collab.concluded_date = datetime.now()
        collab.save()
        messages.info(request, "The collab has been moved to concluded")
        return redirect('collab')
    else:
        return redirect('collab')

@login_required
def unlockCollab(request, id):
    collab = Collab.objects.get(id=id)
    if collab.researcher:
        collab.is_locked = False
        collab.save()
        messages.info(request, "The collab has been unlocked sucessfully")
        return redirect('collab')
    else:
        return redirect('collab')

@login_required
def offerCollab(request, id, user_Id):
    collab = Collab.objects.get(id=id)
    if collab.researcher == request.user:
        for person in collab.interested_people.all():
            if person.user_Id == user_Id:
                # collab.interested_people.remove(person)
                collab.collaborators.add(person)
                entry = Notification()
                entry.owner = person
                entry.sender = request.user
                entry.collab = collab
                entry.message = "has allowed you to collaborate on"
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

        messages.info(request, "The collab has been offered successfully")
        collab.accepted_date = datetime.now()
        collab.save()
        return redirect('show_collab', id)
    else:
        return redirect('collab')

@login_required
def declineCollab(request, id, user_Id):
    collab = Collab.objects.get(id=id)

    if collab.researcher == request.user:
        for person in collab.interested_people.all():
            if person.user_Id == user_Id:
                collab.interested_people.remove(person)

        for person in collab.collaborators.all():
            if person.user_Id == user_Id:
                collab.collaborators.remove(person)

                entry = Notification()
                entry.owner = person
                entry.sender = request.user
                entry.collab = collab
                entry.message = "declined your collaboration on"
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

        messages.info(request, "The collab has been declined successfully")
        collab.save()

        return redirect('show_collab', id)
    else:
        return redirect('collab')

@login_required
def requestRemoveCollab(request, id, user_Id):
    collab = Collab.objects.get(id=id)

    if request.user in collab.collaborators.all():
        for person in collab.collaborators.all():
            if person.user_Id == user_Id:
                collab.request_removed_people.add(person)

                entry = Notification()
                entry.owner = collab.researcher
                entry.sender = person
                entry.collab = collab
                entry.message = "wants to be removed from"
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

        messages.info(request, "The researcher has been notified")
        collab.save()

        return redirect('collab')
    else:
        return redirect('collab')

@login_required
def removeCollab(request, id, user_Id):
    collab = Collab.objects.get(id=id)

    if collab.researcher == request.user:
        for person in collab.collaborators.all():
            if person.user_Id == user_Id:
                collab.removed_people.add(person)

                entry = Notification()
                entry.owner = person
                entry.sender = request.user
                entry.collab = collab
                entry.message = "sought your removal from"
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

        messages.info(request, "The collaborator has been notified")
        collab.save()

        return redirect('show_collab_initiated', id)
    else:
        return redirect('collab')

@login_required
def reportCollaborator(request, id, user_Id):
    collab = Collab.objects.get(id=id)

    if collab.researcher == request.user:
        for person in collab.collaborators.all():
            if person.user_Id == user_Id:
                entry = Report()
                entry.is_reported = True
                entry.complainer = request.user
                entry.collab = collab
                entry.receiver = person
                entry.save()
        messages.info(request, "The reporting has been sent to the admins")

        return redirect('collab')
    else:
        return redirect('collab')

@login_required
def reportResearcher(request, id):
    collab = Collab.objects.get(id=id)
    if request.user in collab.collaborators.all():
        entry = Report()
        entry.is_reported = True
        entry.complainer = request.user
        entry.collab = collab
        entry.receiver = collab.researcher
        entry.save()
        messages.info(request, "The reporting has been sent to the admins")

        return redirect('collab')
    else:
        return redirect('collab')

@login_required
def leaveCollab(request, id, user_Id):
    collab = Collab.objects.get(id=id)
    if request.user in collab.collaborators.all():
        for person in collab.interested_people.all():
            if person.user_Id == user_Id:
                collab.interested_people.remove(person)

        for person in collab.collaborators.all():
            if person.user_Id == user_Id:
                collab.collaborators.remove(person)

        for person in collab.removed_people.all():
            if person.user_Id == user_Id:
                collab.rollab.removed_people.remove(person)

                entry = Notification()
                entry.owner = person
                entry.sender = request.user
                entry.collab = collab
                entry.message = "has left"
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
        messages.info(request, "You have successfully left and the researcher has been notified")
        collab.save()
        return redirect('collab')
    else:
        return redirect('collab')

@login_required
def acceptLeaveCollab(request, id, user_Id):
    collab = Collab.objects.get(id=id)
    if collab.researcher == request.user:
        for person in collab.interested_people.all():
            if person.user_Id == user_Id:
                collab.interested_people.remove(person)

        for person in collab.collaborators.all():
            if person.user_Id == user_Id:
                collab.collaborators.remove(person)

        for person in collab.request_removed_people.all():
            if person.user_Id == user_Id:
                collab.request_removed_people.remove(person)

                entry = Notification()
                entry.owner = person
                entry.sender = request.user
                entry.collab = collab
                entry.message = "has granted your exit and removed you from"
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

        messages.info(request, "The collaborator has been removed successfully")
        collab.save()

        return redirect('show_collab_initiated', id)
    else:
        return redirect('collab')

@login_required
def undoInterestCollab(request, id):
    collab = Collab.objects.get(id=id)
    # for collaborator in collaborators:
    #     collab.interested_people.add(collaborator)
    collab.interested_people.remove(request.user)
    messages.info(request, "Your interest has been undone successfully")
    collab.save()
    return redirect('collab')

@login_required
def collabs(request):
    context = {}
    filtered_initiated_collabs = InitiatedCollabFilter(
        request.GET,
        queryset = Collab.objects.filter(researcher=request.user, is_locked=False)
    )
    context['filtered_initiated_collabs'] = filtered_initiated_collabs
    paginated_filtered_initiated_collabs = Paginator(filtered_initiated_collabs.qs, 100)
    page_number = request.GET.get('page')
    initiated_collabs_page_obj = paginated_filtered_initiated_collabs.get_page(page_number)
    context['initiated_collabs_page_obj'] = initiated_collabs_page_obj
    total_initiated_collabs = filtered_initiated_collabs.qs.count()
    context['total_initiated_collabs'] = total_initiated_collabs

    filtered_accepted_collabs = InitiatedCollabFilter(
        request.GET,
        queryset = Collab.objects.filter(interested_people=request.user, is_locked=False)
    )
    context['filtered_accepted_collabs'] = filtered_accepted_collabs
    paginated_filtered_accepted_collabs = Paginator(filtered_accepted_collabs.qs, 100)
    page_number = request.GET.get('page')
    accepted_collabs_page_obj = paginated_filtered_accepted_collabs.get_page(page_number)
    context['accepted_collabs_page_obj'] = accepted_collabs_page_obj
    total_accepted_collabs = filtered_accepted_collabs.qs.count()
    context['total_accepted_collabs'] = total_accepted_collabs

    return render(request, 'account/collabs.html', context)

@login_required
def initiatedCollabs(request):
    context = {}
    filtered_initiated_collabs = InitiatedCollabFilter(
        request.GET,
        queryset = Collab.objects.filter(researcher=request.user, is_locked = True, is_concluded=False)
    )
    context['filtered_initiated_collabs'] = filtered_initiated_collabs
    paginated_filtered_initiated_collabs = Paginator(filtered_initiated_collabs.qs, 100)
    page_number = request.GET.get('page')
    initiated_collabs_page_obj = paginated_filtered_initiated_collabs.get_page(page_number)
    context['initiated_collabs_page_obj'] = initiated_collabs_page_obj
    total_initiated_collabs = filtered_initiated_collabs.qs.count()
    context['total_initiated_collabs'] = total_initiated_collabs

    return render(request, 'account/initiated_collabs.html', context)

@login_required
def concludedCollabs(request):
    context = {}
    filtered_concluded_collabs = InitiatedCollabFilter(
        request.GET,
        queryset = Collab.objects.filter(researcher=request.user, is_concluded=True)
    )
    context['filtered_concluded_collabs'] = filtered_concluded_collabs
    paginated_filtered_concluded_collabs = Paginator(filtered_concluded_collabs.qs, 100)
    page_number = request.GET.get('page')
    concluded_collabs_page_obj = paginated_filtered_concluded_collabs.get_page(page_number)
    context['concluded_collabs_page_obj'] = concluded_collabs_page_obj
    total_concluded_collabs = filtered_concluded_collabs.qs.count()
    context['total_concluded_collabs'] = total_concluded_collabs

    filtered_concluded2_collabs = InitiatedCollabFilter(
        request.GET,
        queryset = Collab.objects.filter(collaborators=request.user, is_concluded=True)
    )
    context['filtered_concluded2_collabs'] = filtered_concluded2_collabs
    paginated_filtered_concluded2_collabs = Paginator(filtered_concluded2_collabs.qs, 100)
    page_number = request.GET.get('page')
    concluded2_collabs_page_obj = paginated_filtered_concluded2_collabs.get_page(page_number)
    context['concluded2_collabs_page_obj'] = concluded2_collabs_page_obj
    total_concluded2_collabs = filtered_concluded2_collabs.qs.count()
    context['total_concluded2_collabs'] = total_concluded2_collabs

    return render(request, 'account/concluded_collabs.html', context)

@login_required
def acceptedCollabs(request):
    context = {}
    filtered_accepted_collabs = InitiatedCollabFilter(
        request.GET,
        queryset = Collab.objects.filter(collaborators=request.user, is_concluded=False)
    )
    context['filtered_accepted_collabs'] = filtered_accepted_collabs
    paginated_filtered_accepted_collabs = Paginator(filtered_accepted_collabs.qs, 100)
    page_number = request.GET.get('page')
    accepted_collabs_page_obj = paginated_filtered_accepted_collabs.get_page(page_number)
    context['accepted_collabs_page_obj'] = accepted_collabs_page_obj
    total_accepted_collabs = filtered_accepted_collabs.qs.count()
    context['total_accepted_collabs'] = total_accepted_collabs
    return render(request, 'account/accepted_collabs.html', context)

@login_required
def clearUnreads(request):
    try:
        reg = Notification.objects.filter(owner=request.user)[0]
        reg.unreads = 0
        reg.save()
        placeholder = 0
    except:
        placeholder = 0
    reg1 = Researcher.objects.get(username=request.user.username)
    reg1.bell_unreads = placeholder
    reg1.save()
    return redirect('bell_notifications')

@login_required
def showBellNotifications(request):
    context = {}
    filtered_bell_notifications = BellNotificationFilter(
        request.GET,
        queryset = Notification.objects.filter(owner=request.user)
    )
    context['filtered_bell_notifications'] = filtered_bell_notifications
    paginated_filtered_bell_notifications = Paginator(filtered_bell_notifications.qs, 100)
    page_number = request.GET.get('page')
    bell_notifications_page_obj = paginated_filtered_bell_notifications.get_page(page_number)
    context['bell_notifications_page_obj'] = bell_notifications_page_obj
    total_bell_notifications = filtered_bell_notifications.qs.count()
    context['total_bell_notifications'] = total_bell_notifications

    return render(request, 'account/bell_notifications.html', context)

@login_required
def loginTo(request):
    if request.user.type == "Researcher":
        return HttpResponseRedirect(reverse('researcher_board'))
    # elif request.user.type == "QwikA--":
    #     return HttpResponseRedirect(reverse('qwikadmin_board'))
    # elif request.user.type == "QwikVendor":
    #     return HttpResponseRedirect(reverse('qwikvendor_board'))
    # elif request.user.type == "QwikPartner":
    #     return HttpResponseRedirect(reverse('qwikpartner_board'))

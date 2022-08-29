import json
import urllib.request
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomRegisterForm, CollabForm, CustomRegisterFormResearcher, FlagForm
from .models import Collab, Researcher, Notification
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.decorators import login_required, permission_required
from .filters import InitiatedCollabFilter, BellNotificationFilter
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from datetime import datetime

def create(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save(commit=False).email = username
            form.save()
            messages.success(request, "Registration was successful!")
            return redirect('account')
        else:
            messages.error(request, "Please review and correct form input fields")
            #return redirect('account')
    else:
        form = CustomRegisterForm()
    return render(request, 'account/account.html', {'form': form})

# def create(request):
#     if request.method == "POST":
#         form = CustomRegisterForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             recaptcha_response = request.POST.get('g-recaptcha-response')
#             url = 'https://www.google.com/recaptcha/api/siteverify'
#             values = {
#                 'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
#                 'response': recaptcha_response
#             }
#             data = urllib.parse.urlencode(values).encode()
#             req =  urllib.request.Request(url, data=data)
#             response = urllib.request.urlopen(req)
#             result = json.loads(response.read().decode())
#             if result['success']:
#                 user = form.save(commit=False)
#                 user.email = username
#                 user.is_active = False
#                 user.save()
#                 current_site = get_current_site(request)
#                 subject = 'Activate Your Et al. Account'
#                 message = render_to_string('account/account_activation_email.html', {
#                     'user': user,
#                     'domain': current_site.domain,
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token': account_activation_token.make_token(user),
#                 })
#                 user.email_user(subject, message)
#                 messages.success(request, ('Please login to your email, you have been sent a message for email verification.'))
#                 return redirect('login')
#             else:
#                 messages.error(request, "Please ensure you pass reCAPTCHA so as to ascertain that you are human")
#             return redirect('account')
#     else:
#         form = CustomRegisterForm()
#     return render(request, 'account/account.html', {'form': form})

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account has been confirmed! Please complete registration by supplying location information'))
            return redirect('edit_profile')
        else:
            messages.error(request, ('The confirmation link has either been used or expired.'))
            return redirect('login')

@login_required
# @permission_required('users.view_admin')
def showResearcherBoard(request):

    return render(request, 'account/researcher_board.html', {})

@login_required
# @permission_required('users.view_admin')
def showHome(request):

    return render(request, 'account/home.html', {})

# @login_required
# def showCollabs(request):
#     context = {}
#     filtered_collabs = CollabFilter(
#         request.GET,
#         queryset = Collab.objects.all()
#     )
#     context['filtered_collabs'] = filtered_collabs
#     paginated_filtered_collabs = Paginator(filtered_collabs.qs, 30)
#     page_number = request.GET.get('page')
#     collabs_page_obj = paginated_filtered_collabs.get_page(page_number)
#     context['collabs_page_obj'] = collabs_page_obj
#     total_collabs = filtered_collabs.qs.count()
#     context['total_collabs'] = total_collabs
#
#     form = CollabForm()
#     if request.method == 'POST':
#         form = CollabForm(request.POST, request.FILES, None)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "The collab has been created successfully")
#             return redirect('collabs')
#         else:
#             messages.error(request, "Please review form input fields below")
#     context['form'] = form
#
#     return render(request, 'account/collabs.html', context=context)

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

def createCollab(request):
    form = CollabForm(request=request)
    if request.method == 'POST':
        form = CollabForm(request.POST, request.FILES, None, request=request)
        if form.is_valid():
            form.save(commit=False).researcher=request.user
            form.save()
            messages.info(request, "The collab has been created successfully")
            return redirect('create_collab')
        else:
            messages.error(request, "Please review form input fields below")
    return render(request, 'account/create_collab.html', {'form':form})

@login_required
def showResearcherProfile(request, **kwargs):
    if request.method == "POST":
        form = CustomRegisterFormResearcher(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            form.save(commit=False).email = email
            form.save()
            messages.success(request, "Your profile has been modified successfully")
            return redirect('researcher_profile')
        else:
            messages.error(request, "Error: Please review form input fields below")
    else:
        form = CustomRegisterFormResearcher(instance=request.user)
    return render(request, 'account/researcher_profile.html', {'form': form})

@login_required
def showUser(request, email, **kwargs):
    researcher = Researcher.objects.get(username=email)
    context = {'researcher': researcher}
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
    form = CollabForm(instance=collab, request=request)
    if request.method=='POST':
        form = CollabForm(request.POST, instance=collab, request=request)
        if form.is_valid():
            form.save()
            messages.info(request, "The collab has been updated successfully")
            return redirect('collab')
    return render(request, 'account/update_collab.html', {'form': form, 'collab':collab})

@login_required
def deleteCollab(request, id):
    collab = Collab.objects.get(id=id)
    obj = get_object_or_404(Collab, id=id)
    if request.method =="POST":
        obj.delete()
        messages.info(request, "The collab has been deleted successfully")
        return redirect('collab')
    return render(request, 'account/collab_confirm_delete.html', {'collab':collab})

@login_required
def showCollabInitiated(request, id, **kwargs):
    collab = Collab.objects.get(id=id)
    counter = 0
    for person in collab.collaborators.all():
        counter += 1
    context = {'collab': collab, 'counter':counter}
    return render(request, 'account/collab_initiated.html', context)

@login_required
def showCollabAccepted(request, id, **kwargs):
    collab = Collab.objects.get(id=id)
    counter = 0
    for person in collab.collaborators.all():
        counter += 1

    context = {'collab': collab, 'counter':counter}
    return render(request, 'account/collab_accepted.html', context)

# @login_required
# @permission_required('users.view_admin')
# def showQwikAdminBoard(request):
#     people = Person.objects.all().count()
#     qwikcustomers = Person.objects.filter(type="QwikCustomer").count()
#     qwikvendors = Person.objects.filter(type="QwikVendor").count()
#     qwikpartners = Person.objects.filter(type="QwikPartner").count()
#     qwikadmins = Person.objects.filter(type="QwikA--").count()
#
#     perc_cust = round((qwikcustomers/people)*100,1)
#     perc_vend = round((qwikvendors/people)*100,1)
#     perc_part = round((qwikpartners/people)*100,1)
#     perc_adm = round((qwikadmins/people)*100,1)
#
#     cust = round(perc_cust/100,2)
#     vend = round(perc_vend/100,2)
#     part = round(perc_part/100,2)
#     adm = round(perc_adm/100,2)
#
#     return render(request, 'users/qwikadmin_board.html', {'qwikcustomers':qwikcustomers,
#                                                           'perc_cust':perc_cust,
#                                                           'qwikvendors':qwikvendors,
#                                                           'perc_vend':perc_vend,
#                                                           'qwikpartners':qwikpartners,
#                                                           'perc_part':perc_part,
#                                                           'qwikadmins':qwikadmins,
#                                                           'perc_adm':perc_adm,
#                                                           'cust':cust,
#                                                           'vend':vend,
#                                                           'part':part,
#                                                           'adm':adm})

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
    entry.message = "A new collaborator showed interest on"
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
    collab.is_locked = True
    collab.locked_date = datetime.now()
    collab.save()
    messages.info(request, "The collab has been locked sucessfully")
    return redirect('collab')

@login_required
def unlockCollab(request, id):
    collab = Collab.objects.get(id=id)
    collab.is_locked = False
    collab.save()
    messages.info(request, "The collab has been unlocked sucessfully")
    return redirect('collab')

@login_required
def offerCollab(request, id, username):
    collab = Collab.objects.get(id=id)

    for person in collab.interested_people.all():
        if person.username == username:
            collab.interested_people.remove(person)
            collab.collaborators.add(person)

            entry = Notification()
            entry.owner = person
            entry.sender = request.user
            entry.collab = collab
            entry.message = "You have been allowed to collaborate on"
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
        queryset = Collab.objects.filter(Q(researcher=request.user) | Q(interested_people=request.user), is_locked=False)
    )
    context['filtered_initiated_collabs'] = filtered_initiated_collabs
    paginated_filtered_initiated_collabs = Paginator(filtered_initiated_collabs.qs, 100)
    page_number = request.GET.get('page')
    initiated_collabs_page_obj = paginated_filtered_initiated_collabs.get_page(page_number)
    context['initiated_collabs_page_obj'] = initiated_collabs_page_obj
    total_initiated_collabs = filtered_initiated_collabs.qs.count()
    context['total_initiated_collabs'] = total_initiated_collabs

    return render(request, 'account/collabs.html', context)

@login_required
def initiatedCollabs(request):
    context = {}
    filtered_initiated_collabs = InitiatedCollabFilter(
        request.GET,
        queryset = Collab.objects.filter(researcher=request.user, is_locked = True)
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
def acceptedCollabs(request):
    context = {}
    filtered_accepted_collabs = InitiatedCollabFilter(
        request.GET,
        queryset = Collab.objects.filter(collaborators=request.user)
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
    try:
        reg = Notification.objects.filter(owner=request.user)[0]
        reg.unreads = 0
        reg.save()
        placeholder = 0
    except:
        pass
    reg1 = Researcher.objects.get(username=request.user.username)
    reg1.bell_unreads = placeholder
    reg1.save()

    return render(request, 'account/bell_notifications.html', context)

@login_required
def loginTo(request):
    if request.user.type == "Researcher/Collaborator":
        return HttpResponseRedirect(reverse('researcher_board'))
    # elif request.user.type == "QwikA--":
    #     return HttpResponseRedirect(reverse('qwikadmin_board'))
    # elif request.user.type == "QwikVendor":
    #     return HttpResponseRedirect(reverse('qwikvendor_board'))
    # elif request.user.type == "QwikPartner":
    #     return HttpResponseRedirect(reverse('qwikpartner_board'))

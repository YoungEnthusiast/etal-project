import json
import urllib.request
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomRegisterForm, CollabForm
from .models import Collab
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.decorators import login_required, permission_required
from .filters import CollabFilter
from django.core.paginator import Paginator
from django.core.mail import send_mail
# from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

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

@login_required
def showCollabs(request):
    context = {}
    filtered_collabs = CollabFilter(
        request.GET,
        queryset = Collab.objects.all()
    )
    context['filtered_collabs'] = filtered_collabs
    paginated_filtered_collabs = Paginator(filtered_collabs.qs, 30)
    page_number = request.GET.get('page')
    collabs_page_obj = paginated_filtered_collabs.get_page(page_number)
    context['collabs_page_obj'] = collabs_page_obj
    total_collabs = filtered_collabs.qs.count()
    context['total_collabs'] = total_collabs

    form = CollabForm()
    if request.method == 'POST':
        form = CollabForm(request.POST, request.FILES, None)
        if form.is_valid():
            form.save()
            messages.success(request, "The collab has been created successfully")
            return redirect('collabs')
        else:
            messages.error(request, "Please review form input fields below")
    context['form'] = form

    return render(request, 'account/collabs.html', context=context)

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
def loginTo(request):
    if request.user.type == "Researcher":
        return HttpResponseRedirect(reverse('researcher_board'))
    # elif request.user.type == "QwikA--":
    #     return HttpResponseRedirect(reverse('qwikadmin_board'))
    # elif request.user.type == "QwikVendor":
    #     return HttpResponseRedirect(reverse('qwikvendor_board'))
    # elif request.user.type == "QwikPartner":
    #     return HttpResponseRedirect(reverse('qwikpartner_board'))

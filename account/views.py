import json
import urllib.request
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomRegisterForm, ProfileEditForm, ProductCustomerEditForm, AdminCreditForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, login
from orders.models import UserOrder, VisitorOrder, OrderItem, VisitorOrderItem, OrderStatus
from products.models import Product
from products.filters import UserOrderFilter, UserOrderFilter2, TrackFilter
from orders.forms import UserOrderForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required
from .models import ProductCustomer, ProductWalletHistorie
from xplorers.models import XploreCustomer
from .filters import ProductWalletHistorieFilter
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.views.generic import View, UpdateView
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token


from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .forms import CustomRegisterForm

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

# @login_required
# def loginTo(request):
#     if request.user.type == "Researcher":
    #     return HttpResponseRedirect(reverse('qwikcust_board'))
    # elif request.user.type == "QwikA--":
    #     return HttpResponseRedirect(reverse('qwikadmin_board'))
    # elif request.user.type == "QwikVendor":
    #     return HttpResponseRedirect(reverse('qwikvendor_board'))
    # elif request.user.type == "QwikPartner":
    #     return HttpResponseRedirect(reverse('qwikpartner_board'))

def create(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            if result['success']:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate Your BuildQwik Account'
                message = render_to_string('users/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                messages.success(request, ('Please login to your email, you have been sent a message for email verification.'))
                return redirect('login')
            else:
                messages.error(request, "Please ensure you pass reCAPTCHA so as to ascertain that you are human")
            return redirect('account')
    else:
        form = CustomRegisterForm()
    return render(request, 'users/account.html', {'form': form})

# def create(request):
#     if request.method == "POST":
#         form = CustomRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             subject = 'Activate Your BuildQwik Account'
#             message = render_to_string('users/account_activation_email0.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             user.email_user(subject, message)
#             messages.success(request, ('Please login to your email, you have been sent a message for email verification.'))
#             return redirect('login')
#         else:
#             messages.error(request, 'A user with the supplied username or email already exists')
#         return redirect('account')
#     else:
#         form = CustomRegisterForm()
#     return render(request, 'users/account.html', {'form': form})



class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.productcustomer.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account has been confirmed! Please complete registration by supplying location information'))
            return redirect('edit_profile')
        else:
            messages.warning(request, ('The confirmation link has either been used or expired.'))
            return redirect('index')

@login_required
def editProfile(request, **kwargs):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        customer_form = ProductCustomerEditForm(request.POST, request.FILES, instance=request.user.productcustomer)
        if form.is_valid() and customer_form.is_valid():
            form.save()
            customer_form.save()
            new_customer = ProductCustomer.objects.get(user=request.user)
            new_customer.save()
            try:
                if new_customer.CAC_Certificate == "":
                    pass
                else:
                    new_xplorer = XploreCustomer()
                    new_xplorer.user = new_customer.user
                    new_xplorer.phone_Number = new_customer.phone_Number
                    new_xplorer.state = new_customer.state
                    new_xplorer.city = new_customer.city
                    new_xplorer.address = new_customer.address
                    new_xplorer.CAC_Certificate = new_customer.CAC_Certificate
                    new_xplorer.save()
            except:
                new_xplorer = XploreCustomer.objects.get(user=request.user)
                new_xplorer.user = new_customer.user
                new_xplorer.phone_Number = new_customer.phone_Number
                new_xplorer.state = new_customer.state
                new_xplorer.city = new_customer.city
                new_xplorer.address = new_customer.address
                new_xplorer.CAC_Certificate = new_customer.CAC_Certificate
                new_xplorer.save()
            messages.success(request, "Your profile has been modified")
            return redirect('edit_profile')
        else:
            messages.error(request, "Error: Please review form input fields below")
    else:
        form = ProfileEditForm(instance=request.user)
        customer_form = ProductCustomerEditForm(instance=request.user.productcustomer)
    return render(request, 'users/edit_profile.html', {'form': form, 'customer_form': customer_form})

from django.shortcuts import render
from django.urls import reverse_lazy, reverse

def login(request):
    render(request, 'registration/login.html')
#
# def create(request):
#     if request.method == "POST":
#         form = CustomRegisterForm(request.POST, request.FILES)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             form.save(commit=False).email = username
#             form.save()
#             messages.success(request, "Registration was successful!")
#             return redirect('account')
#         else:
#             messages.error(request, "Please review and correct form input fields")
#             #return redirect('account')
#     else:
#         form = CustomRegisterForm()
#     return render(request, 'account/account.html', {'form': form})

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

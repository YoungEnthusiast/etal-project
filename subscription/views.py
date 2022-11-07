from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required, permission_required
from .models import Subscription
from dateutil.rrule import rrule, DAILY
import calendar

@login_required
def plans(request):
    return render(request, 'subscription/plans.html')

@login_required
def upgrade(request):
    monthly = 5
    yearly = 50
    key = 'pk_test_8b5034b6a82fb45ee0f2662d339845ca48d7d8e8'

    context = {'monthly':monthly, 'yearly':yearly, 'key':key}
    return render(request, 'subscription/upgrade_page.html', context)

@login_required
def history(request):
    today = datetime.now()
    try:
        reg = Subscription.objects.filter(user=request.user)[0]
        current_bill = reg.current_bill
        last_payment = reg.last_payment
        next_payment = reg.subscription_ends
        subscription_type = reg.subscription_type
    except:
        current_bill = None
        last_payment = None
        next_payment = None
        subscription_type = None
    try:
        reg1 = Subscription.objects.filter(user=request.user)[0]
        if today <= reg1.subscription_ends:
            okay = "Yes"
        else:
            okay = 'No'
    except:
        okay ="No"

    context = {'current_bill':current_bill, 'last_payment':last_payment, 'next_payment':next_payment, 'subscription_type':subscription_type, 'okay':okay}
    return render(request, 'subscription/history.html', context)

@login_required
def monthly(request):
    today = datetime.now()
    current_year = today.strftime("%Y")
    current_month = today.strftime("%m")
    new_entry = Subscription()
    new_entry.user = request.user
    new_entry.last_payment = today
    new_entry.subscription_type = "Monthly"
    new_entry.current_bill = "$5 per month"
    new_entry.subscription_ends = today + timedelta(days=int(calendar.monthrange(int(current_year), int(current_month))[1]))
    new_entry.save()
    return redirect('upgrade')

    # fulls = Subscription.objects.filter(package='Full Width', subscription_Ends__gte=date.today())
    # three_quarters = Subscription.objects.filter(package='Three Quarters', subscription_Ends__gte=date.today())
    # one_quarters = Subscription.objects.filter(package='One Quarter', subscription_Ends__gte=date.today())
    # context = {}
    # return render(request, 'xplorers/xplore.html', context)

@login_required
def yearly(request):
    today = datetime.now()
    current_year = int(today.strftime("%Y"))

    if current_year/4 == 0:
        days = 366
    else:
        days = 365

    new_entry = Subscription()
    new_entry.user = request.user
    new_entry.last_payment = today
    new_entry.subscription_type = "Yearly"
    new_entry.current_bill = "$50 per year"
    new_entry.subscription_ends = today + timedelta(days=days)
    new_entry.save()
    return redirect('upgrade')

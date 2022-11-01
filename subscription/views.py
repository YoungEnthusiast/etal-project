from django.shortcuts import render


def plans(request):
    return render(request, 'subscription/plans.html')

def upgrade(request):
    monthly = 5
    yearly = 60
    key = 'pk_test_8b5034b6a82fb45ee0f2662d339845ca48d7d8e8'
    context = {'monthly':monthly, 'yearly':yearly, 'key':key}
    return render(request, 'subscription/upgrade_page.html', context)

def history(request):

    context = {}
    return render(request, 'subscription/history.html', context)

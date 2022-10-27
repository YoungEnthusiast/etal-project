from django.shortcuts import render


def plans(request):
    return render(request, 'subscription/plans.html')

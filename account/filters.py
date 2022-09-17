import django_filters as filters
# from django_filters import DateFilter, CharFilter
from .models import Collab, Notification, CollabDoc, Task
# from django.forms.widgets import NumberInput
# from django.db.models import Q

class InitiatedCollabFilter(filters.FilterSet):
    # start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    # start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    # q = CharFilter(method='my_custom_filter',label="Others")

    class Meta:
        model = Collab
        fields = []
    # def my_custom_filter(self, queryset, name, value):
    #     return queryset.filter(Q(user__username__icontains=value) | Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value) | Q(payment_choice__icontains=value) | Q(payment_type1__icontains=value) | Q(payment_type2__icontains=value) | Q(payment_type3__icontains=value) | Q(transaction__icontains=value))

class BellNotificationFilter(filters.FilterSet):
    # start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    # start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    # q = CharFilter(method='my_custom_filter',label="Others")

    class Meta:
        model = Notification
        fields = []

class CollabDocFilter(filters.FilterSet):
    # start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    # start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    # q = CharFilter(method='my_custom_filter',label="Others")

    class Meta:
        model = CollabDoc
        fields = []

class TaskFilter(filters.FilterSet):
    # start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    # start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    # q = CharFilter(method='my_custom_filter',label="Others")

    class Meta:
        model = Task
        fields = []

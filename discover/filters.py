import django_filters as filters
# from django_filters import DateFilter, CharFilter
from .models import Post
# from django.forms.widgets import NumberInput
# from django.db.models import Q

class PostFilter(filters.FilterSet):
    # start_date = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='gte', label='Dates Above', widget=NumberInput(attrs={'type': 'date'}))
    # start_date2 = DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'], field_name="created", lookup_expr='lte', label='Dates Below', widget=NumberInput(attrs={'type': 'date'}))
    # q = CharFilter(method='my_custom_filter',label="Others")

    class Meta:
        model = Post
        fields = []

import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
    created_date = DateFilter(field_name="created_date", lookup_expr='gte')
    Title = CharFilter(field_name="title", lookup_expr='icontains' )
    class Meta:
        model = Ticket
        fields = '__all__'
        exclude = ['project', 'id_in_project', 'description', 'updated_date', 'title']
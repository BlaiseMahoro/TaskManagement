import django_filters
from django_filters import DateFilter, CharFilter, ChoiceFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
    
    Title = CharFilter(field_name="title", lookup_expr='icontains' )
    Assignees = ChoiceFilter(field_name="assignees")
    class Meta:
        model = Ticket
        fields = '__all__'
        exclude = ['project', 'id_in_project', 'description','created_date', 'updated_date', 'title', 'assignees']
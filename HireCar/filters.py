import django_filters
from .models import *

class CarFilter(django_filters.FilterSet):
    min_mileage = django_filters.NumberFilter(field_name='mileage', lookup_expr='gte', label='Min Mileage')
    max_mileage = django_filters.NumberFilter(field_name='mileage', lookup_expr='lte', label='Max Mileage')

    min_rate = django_filters.NumberFilter(field_name='daily_rate', lookup_expr='gte', label='Min Daily Rate')
    max_rate = django_filters.NumberFilter(field_name='daily_rate', lookup_expr='lte', label='Max Daily Rate')

    # Other exact-match or general filters
    make = django_filters.CharFilter(lookup_expr='icontains')
    model = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter()
    car_type = django_filters.ModelChoiceFilter(
        queryset=CarType.objects.all(),
        label="Car Type"
    )
    seats = django_filters.NumberFilter()
    transmission = django_filters.CharFilter(lookup_expr='icontains')
    fuel_type = django_filters.CharFilter(lookup_expr='icontains')
    #features = django_filters.CharFilter(lookup_expr='icontains')
    availability = django_filters.BooleanFilter()

    class Meta:
        model = Car
        fields = [
            'make', 'model', 'year', 'car_type', 'seats',
            'transmission', 'fuel_type',
            'availability','min_mileage','max_mileage','min_rate','max_rate'
        ]

'''
    def filter_min_mileage(self, queryset, name, value):
        # If the value is an integer, convert it to float
        if value:
            value = float(value)  # Convert integer to float if provided as an integer
        return queryset.filter(**{name + '__gte': value})

    def filter_max_mileage(self, queryset, name, value):
        if value:
            value = float(value)
        return queryset.filter(**{name + '__lte': value})

    def filter_min_rate(self, queryset, name, value):
        if value:
            value = decimal.Decimal(value)  # Convert to Decimal for proper filtering
        return queryset.filter(**{name + '__gte': value})

    def filter_max_rate(self, queryset, name, value):
        if value:
            value = decimal.Decimal(value)
        return queryset.filter(**{name + '__lte': value})
'''


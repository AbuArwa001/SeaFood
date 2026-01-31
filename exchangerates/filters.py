
# from django_filters.filterset import FilterSet
import django_filters as filters
from exchangerates.models import ExchangeRate
# import rest_framework_filters as filters


class ExchangeRateFilter(filters.FilterSet):
    from_currency__code = filters.CharFilter(field_name='from_currency__code', lookup_expr='iexact')
    to_currency__code = filters.CharFilter(field_name='to_currency__code', lookup_expr='iexact')
    rate_date = filters.DateFromToRangeFilter(field_name='rate_date')
    currencies = filters.CharFilter(method='filter_currencies')

    class Meta:
        model = ExchangeRate
        fields = ['from_currency__code', 'to_currency__code', 'rate_date', 'currencies']

    def filter_currencies(self, queryset, name, value):
        if value:
            currency_codes = [code.strip() for code in value.split(',')]
            return queryset.filter(from_currency__code__in=currency_codes)
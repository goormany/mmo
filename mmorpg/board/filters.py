from django_filters import FilterSet, ChoiceFilter
from .models import ResponsePost, Post


class RequestsFilter(FilterSet):

    class Meta:
        model = ResponsePost
        fields = ['status']
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ListCalculator


urlpatterns = {
    url(r'^shipmodel/$', ListCalculator.as_view(), name='my-view'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
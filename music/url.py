from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ListUsers


urlpatterns = {
    url(r'^shipmodel/$', ListUsers.as_view(), name='my-view'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
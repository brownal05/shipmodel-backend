from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ListCalculator ,VslViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'vsl', VslViewSet)

urlpatterns = {
    url(r'^shipmodel/$', ListCalculator.as_view(), name='my-view'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
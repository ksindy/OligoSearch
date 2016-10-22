from django.conf.urls import url, include
from . import views

app_name = 'conversions'

urlpatterns = [
    url(r'^$', views.test),
    ]
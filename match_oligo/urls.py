from django.conf.urls import url, include
from . import views

app_name = 'oligo'

urlpatterns = [
    url(r'^$', views.import_excel_view),
    ]
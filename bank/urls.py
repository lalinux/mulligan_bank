from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.AccountDetail.as_view(), name='account_detail'),
]
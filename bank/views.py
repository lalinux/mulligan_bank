from django.views.generic import DetailView
from .models import Account


class AccountDetail(DetailView):
    model = Account

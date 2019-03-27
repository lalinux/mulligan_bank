from django.views.generic import ListView

from bank.models import Account


class HomeView(ListView):

    template_name = 'index.html'
    queryset = Account.objects.order_by('-created_at')

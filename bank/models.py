from django.db import models


class Account(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


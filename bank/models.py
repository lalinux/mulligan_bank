from django.db import models
from django.urls import reverse


class Account(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "[Bank Account #%d belongs to %s, is %s and has a balance of $%d" % \
               (
                   self.id,
                   self.owner.get_username(),
                   'active' if self.active else 'not active',
                   self.balance
               )

    def get_absolute_url(self):
        return reverse('account_detail', kwargs={'pk': self.pk})

    def deposit(self, amount):
        if not self.active:
            raise AttributeError("The account is not active, you cannot deposit here")

        if amount > 0:
            self.movements.create(amount=amount)
            self.balance += amount
            self.save()
        else:
            raise ValueError("Deposit amount should be > 0")

    def withdrawal(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount should be > 0")
        if amount > self.balance:
            raise ValueError("Withdrawal amount should be more than balance")
        self.movements.create(amount=amount * -1)
        self.balance -= amount
        self.save()

    def record_history(self):
        return self.movements.all()


class Movement(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="movements")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True, editable=False)

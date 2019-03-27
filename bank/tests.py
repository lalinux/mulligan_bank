import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Account


class AccountModelTest(TestCase):
    username = 'client_1234'

    def setUp(self):
        self.user = get_user_model().objects.create(username=self.username)

    def test_string_representation(self):
        account = Account(owner=self.user)
        account.save()
        self.assertEqual(str(account),
                         "[Bank Account #1 belongs to %s, is active and has a balance of $0" % self.username)

    @unittest.expectedFailure
    def test_owner_not_empty(self):
        account = Account()
        account.save()

    def test_balance_default_0(self):
        account = Account(owner=self.user)
        account.save()
        self.assertEqual(0, account.balance)

    def test_deposit(self):
        account = Account(owner=self.user)
        account.save()
        account.deposit(200)
        self.assertEqual(200, account.balance)

    def test_withdrawal(self):
        account = Account(owner=self.user)
        account.save()
        account.deposit(200)
        account.withdrawal(100)
        self.assertEqual(100, account.balance)

    def test_record_history(self):
        account = Account(owner=self.user)
        account.save()
        account.deposit(200)
        account.withdrawal(100)
        self.assertEqual(2, len(account.record_history()))

    @unittest.expectedFailure
    def test_deposits_inactive(self):
        account = Account(owner=self.user, active=False)
        account.save()
        account.deposit(100)

    @unittest.expectedFailure
    def test_deposits_negative(self):
        account = Account(owner=self.user)
        account.save()
        account.deposit(-100)

    @unittest.expectedFailure
    def test_withdrawal_without_enough_funds(self):
        account = Account(owner=self.user)
        account.save()
        account.withdrawal(100)

    @unittest.expectedFailure
    def test_withdrawal_negative(self):
        account = Account(owner=self.user)
        account.save()
        account.withdrawal(-100)

    def test_get_absolute_url(self):
        account = Account(owner=self.user)
        account.save()
        self.assertIsNotNone(account.get_absolute_url())


class ProjectTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='client_1234')

    def test_one_account(self):
        Account.objects.create(owner=self.user, balance=100, active=True)
        response = self.client.get('/')
        self.assertContains(response, self.user.get_username())
        self.assertContains(response, "$100.00")

    def test_two_account(self):
        Account.objects.create(owner=self.user, balance=100, active=True)
        Account.objects.create(owner=self.user, balance=200, active=True)
        response = self.client.get('/')
        self.assertContains(response, self.user.get_username())
        self.assertContains(response, "$100.00")
        self.assertContains(response, "$200.00")

    def test_no_accounts(self):
        response = self.client.get('/')
        self.assertContains(response, 'No accounts created yet.')


class AccountViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='client_1234')
        self.account = Account.objects.create(owner=self.user, balance=100, active=True)

    def test_basic_view(self):
        response = self.client.get(self.account.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_title_in_entry(self):
        response = self.client.get(self.account.get_absolute_url())
        self.assertContains(response, self.account.owner.username)

from django.test import TestCase
from model_bakery import baker

from accounts.models import Products


class TestUser(TestCase):
    def test_model_user(self):
        product = Products.objects.create(name='a30', brand='sumsong',count=3,price=820000)
        self.assertEqual(str(product), 'a30-sumsung-3-820000')

    def test_create_user(self):
        product = baker.make(Products,name='a30', brand='sumsong',count=3,price=820000)
        self.assertEqual(str(product), 'a30-sumsung-3-820000')
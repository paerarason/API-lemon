from django.test import TestCase
from .models import MenuItem
# Create your tests here.
class MenuItemTest(TestCase):
    def test_get_item(self):
        item=MenuItem.create(title="ICECREAM",price=890,inventory=90,)
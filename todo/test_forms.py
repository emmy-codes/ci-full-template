from django.test import TestCase
from .forms import ItemForm

class TestItemForm(TestCase):
    def test_item_name_is_required()
from django.test import TestCase
from .models import Item
from django.urls import reverse

# Create your tests here.


class TestViews(TestCase):

    def test_get_todo_list(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/todo_list.html")

    def test_get_add_item_page(self):
        response = self.client.get("/add")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/add_item.html")


    def test_get_edit_item_page(self):
        # Create the item using the provided URL for item creation
        response = self.client.post(reverse("add_item"), {"name": "Test Todo Item"})
        self.assertRedirects(response, reverse("get_todo_list"))

        # Retrieve the created item from the database
        item = Item.objects.get(name="Test Todo Item")

        # Attempt to edit the item (you may need to adjust this based on your actual edit view URL)
        response = self.client.get(reverse("edit_item", args=[item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/edit_item.html")

    def test_can_add_item(self):
        response = self.client.post("/add", {"name": "Test Added Item"})
        self.assertRedirects(response, "/")

    def test_can_delete_item(self):
        # Create the item using the provided URL for item creation
        response = self.client.post(reverse("add_item"), {"name": "Test Todo Item"})
        self.assertRedirects(response, reverse("get_todo_list"))

        # Retrieve the created item from the database
        item = Item.objects.get(name="Test Todo Item")

        # Attempt to delete the item
        response = self.client.get(reverse("delete_item", args=[item.id]))
        self.assertRedirects(response, reverse("get_todo_list"))

        # Verify that the item has been deleted from the database
        existing_items = Item.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 0)

    def test_can_toggle_item(self):
        item = Item.objects.create(name="Test Todo Item", done=True)
        response = self.client.get(f"/toggle/{item.id}")
        self.assertRedirects(response, "/")
        updated_item = Item.objects.get(id=item.id)
        self.assertFalse(updated_item.done)

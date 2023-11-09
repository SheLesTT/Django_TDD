from django.test import TestCase
from django.urls import resolve
from ..views import home_page
from ..models import Item, List
from django.http import HttpRequest
class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        respose = self.client.get("/lists/")
        self.assertTemplateUsed(respose, "home.html")



class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_validation_errors_are_send_back_to_home_page(self):

        response = self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        error_message = "You can not have empty list"
        self.assertContains(response, error_message)

    def test_empty_list_is_not_saved(self):

        response = self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):

    def test_uses_new_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")
    def test_displays_all_list_items(self):
        correct_list = List.objects.create()

        Item.objects.create(text="itemey 1", list =correct_list)
        Item.objects.create(text="itemey 2", list = correct_list)
        onther_list = List.objects.create()

        Item.objects.create(text= "tata", list = onther_list)
        Item.objects.create(text = "tete", list= onther_list)
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "tata")
        self.assertNotContains(response, "tete")

class NewItemTest(TestCase):
    def test_add_new_item_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data = {"item_text": "new item for the list"})

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, "new item for the list")
        self.assertEqual(item.list, correct_list)
    def test_redirect_to_a_new_list(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response=self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data = {"item_text": "new item for the list"})

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    def test_passes_correct_list_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}")


        # self.assertEqual(response.context["list"], correct_list)

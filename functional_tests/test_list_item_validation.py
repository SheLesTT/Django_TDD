from selenium.webdriver import Keys

from .base import  FunctionalTest
from selenium.webdriver.common.by import By
class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list(self):

        self.browser.get(self.live_server_url +"/lists/")
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(self.browser.find_element(By.CSS_SELECTOR, "has-error").text,
                         "You can not have an empty list item"))


        self.browser.find_element(By.ID, "id_new_item").send_keys("buy milk")
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        self.wait_for_item_in_table("1: buy milk")

        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(self.browser.find_element(By.CSS_SELECTOR, "has-error").text,
                                               "You can not have an empty list item"))

        self.browser.find_element(By.ID, "id_new_item").send_keys("buy toy")
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        self.wait_for_item_in_table("1: buy milk")
        self.wait_for_item_in_table("2: buy toy")

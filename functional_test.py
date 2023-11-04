import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_item_in_a_list(self, item_text):
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(item_text, [row.text for row in rows],
                      f"New item did not appear in the table contents were {table.text}", )

    def test_can_start_a_list_and_retrieve_it_later(self):

        self.browser.get("http://127.0.0.1:8000/lists/")

        assert "To-Do" in self.browser.title
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertIn(inputbox.get_attribute("placeholder"), "Enter a To-Do item")

        inputbox.send_keys("Buy peacock feathers")
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)

        self.check_item_in_a_list("1: Buy peacock feathers")
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Use peacock feathers to make a fly")
        input_box.send_keys(Keys.ENTER)

        self.check_item_in_a_list("2: Use peacock feathers to make a fly")

        time.sleep(1)


        self.fail("Finish the test!")

if __name__ == '__main__':
    unittest.main(warnings='ignore')
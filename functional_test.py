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

    def test_can_start_a_list_and_retrieve_it_later(self):

        self.browser.get("http://127.0.0.1:8000/")

        assert "To-Do" in self.browser.title
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertIn(inputbox.get_attribute("placeholder"), "Enter a To-Do item")

        inputbox.send_keys("Buy peacock feathers")

        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn("1: Buy peacock feathers", [row.text for row in rows])

        self.fail("Finish the test!")

if __name__ == '__main__':
    unittest.main(warnings='ignore')
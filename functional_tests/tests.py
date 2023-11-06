import os
import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import unittest

MAX_WAIT = 1
class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_item_in_table(self, item_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(item_text, [row.text for row in rows],
                              f"New item did not appear in the table contents were {table.text}", )
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_layout_styling(self):

        self.browser.get(self.live_server_url+"/lists/")
        self.browser.set_window_size(1024,720)

        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEquals(inputbox.location['x']+ inputbox.size['width']/2,
                                512,
                                delta = 10)


    def test_can_start_a_list_for_one_user(self):

        print(self.live_server_url +"/lists/")
        self.browser.get(self.live_server_url +"/lists/")

        assert "To-Do" in self.browser.title
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertIn(inputbox.get_attribute("placeholder"), "Enter a To-Do item")

        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_item_in_table("1: Buy peacock feathers")
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Use peacock feathers to make a fly")
        input_box.send_keys(Keys.ENTER)


        self.wait_for_item_in_table("2: Use peacock feathers to make a fly")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url +"/lists/")
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_item_in_table("1: Buy peacock feathers")

        alice_url = self.browser.current_url
        print(alice_url)
        self.assertRegex(alice_url, "/lists/.+")

        self.browser.quit()
        self.browser = webdriver.Chrome()

        self.browser.get(self.live_server_url +"/lists/")
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_item_in_table("1: Buy milk")

        franck_url = self.browser.current_url
        self.assertRegex(franck_url, "/lists/.+")
        self.assertNotEqual(alice_url, franck_url)

        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)



        self.fail("Finish the test!")

if __name__ == '__main__':
    unittest.main(warnings='ignore')
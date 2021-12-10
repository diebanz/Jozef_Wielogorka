# from django.test import TestCase

# Create your tests here.
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# import chromedriver


class SeleniumTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.user = User.objects.create_superuser(
            username="testuser", password="password"
        )

    def tearDown(self):
        self.user.delete()

    def test_add_post_post(self):
        self.driver.get(f"{self.live_server_url}/admin/")
        sleep(1)
        username_field = self.driver.find_element_by_id("id_username")
        username_field.send_keys("testuser")
        sleep(1)
        password_field = self.driver.find_element_by_id("id_password")
        password_field.send_keys("password")
        sleep(1)
        login_button = self.driver.find_element_by_css_selector(
            "#login-form > div.submit-row > input[type=submit]"
        )
        login_button.click()
        sleep(1)
        self.driver.get(f"{self.live_server_url}/admin/news/news")
        sleep(1)
        rows_before = len(self.driver.find_elements_by_xpath("//table/tbody/tr"))
        add_post_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='content-main']/ul/li/a",
                )
            )
        )
        add_post_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_title"))
        )
        sleep(1)
        title_fields = self.driver.find_elements_by_css_selector("#id_title")
        body_fields = self.driver.find_elements_by_css_selector("#id_body")
        self.assertEqual(len(title_fields), 1)
        self.assertEqual(len(body_fields), 1)
        title_field = self.driver.find_element_by_id("id_title")
        title_field.send_keys("This is a test post")
        sleep(1)
        body_field = self.driver.find_element_by_id("id_body")
        body_field.send_keys(
            "Tempor sunt eu irure do minim in non mollit officia ut in in aute."
        )
        sleep(1)
        submit_button = self.driver.find_element_by_xpath(
            "//*[@id='news_form']/div/div/input[1]"
        )
        submit_button.click()
        sleep(1)
        rows_after = len(self.driver.find_elements_by_xpath("//table/tbody/tr"))
        sleep(1)
        self.assertEqual(rows_before + 1, rows_after)

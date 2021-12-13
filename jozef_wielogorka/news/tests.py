# from django.test import TestCase

# Create your tests here.
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import News


class SeleniumTest(LiveServerTestCase):
    def setUp(self):
        chrome_service = Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        )
        chrome_options = Options()
        options = [
            "--headless",
            "--disable-gpu",
            "--window-size=1920,1200",
            "--ignore-certificate-errors",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ]
        for option in options:
            chrome_options.add_argument(option)
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.user = User.objects.create_superuser(
            username="testuser", password="password"
        )
        News.objects.create(title="Initial News setup", body="This is a news post.")

    def tearDown(self):
        self.user.delete()

    def test_add_news_post(self):
        self.driver.get(f"{self.live_server_url}/admin/")
        username_field = self.driver.find_element_by_id("id_username")
        username_field.send_keys("testuser")
        password_field = self.driver.find_element_by_id("id_password")
        password_field.send_keys("password")
        login_button = self.driver.find_element_by_css_selector(
            "#login-form > div.submit-row > input[type=submit]"
        )
        login_button.click()
        self.driver.get(f"{self.live_server_url}/admin/news/news")
        rows_before = len(self.driver.find_elements_by_xpath("//table/tbody/tr"))
        entries_before = len(News.objects.all())
        add_news_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='content-main']/ul/li/a",
                )
            )
        )
        add_news_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_title"))
        )
        title_fields = self.driver.find_elements_by_css_selector("#id_title")
        body_fields = self.driver.find_elements_by_css_selector("#id_body")
        self.assertEqual(len(title_fields), 1)
        self.assertEqual(len(body_fields), 1)
        title_field = self.driver.find_element_by_id("id_title")
        title_field.send_keys("This is a test post")
        body_field = self.driver.find_element_by_id("id_body")
        body_field.send_keys(
            "Tempor sunt eu irure do minim in non mollit officia ut in in aute."
        )
        submit_button = self.driver.find_element_by_xpath(
            "//*[@id='news_form']/div/div/input[1]"
        )
        submit_button.click()
        rows_after = len(self.driver.find_elements_by_xpath("//table/tbody/tr"))
        entries_after = len(News.objects.all())
        self.assertEqual(rows_before + 1, rows_after)
        self.assertEqual(entries_before + 1, entries_after)

    def test_view_news_post(self):
        try:
            self.driver.set_page_load_timeout(1)
            self.driver.get(f"{self.live_server_url}/")
        except Exception:
            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE)
        title_field = self.driver.find_element_by_xpath(
            "/html/body/main/section[1]/div/h2"
        )
        body_field = self.driver.find_element_by_xpath(
            "/html/body/main/section[1]/div/p[1]"
        )
        self.assertTrue(
            ["Initial News setup", "This is a news post."], [title_field, body_field]
        )
        new_title = "Update"
        new_body = "This is an important new development"
        News.objects.create(title=new_title, body=new_body)
        try:
            self.driver.refresh()
        except Exception:
            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE)
        title_field = self.driver.find_element_by_xpath(
            "/html/body/main/section[1]/div/h2"
        )
        body_field = self.driver.find_element_by_xpath(
            "/html/body/main/section[1]/div/p[1]"
        )
        self.assertTrue([new_title, new_body], [title_field, body_field])

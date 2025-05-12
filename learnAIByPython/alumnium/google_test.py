import os
import unittest
from alumnium import Alumni
from selenium.webdriver import Chrome
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Access the API key
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

class TestGoogleSearch(unittest.TestCase):
    def setUp(self):
        page = sync_playwright().start().chromium.launch(headless=False).new_page()
        page.goto("https://todomvc.com/examples/vue/dist")
        self.al = Alumni(page)

    def test_search(self):
        self.al.do("search for 'Mercury element'")
        self.al.do("mark all tasks complete")
        self.al.do("delete all tasks")
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Create your tests here.
class HomepageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        cls.browser = webdriver.Chrome(options=chrome_options)
        cls.page_wait = WebDriverWait(cls.browser, 10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def setUp(self):
        self.browser.get('http://localhost:8000/')
    
    def test_homepage_search(self):
        search_input = self.browser.find_element(By.ID, 'vendor_name')
        search_button = self.browser.find_element(By.ID, 'search_button')
        search_input.send_keys('Adobe')
        search_button.click()

        page_information = self.page_wait.until(EC.text_to_be_present_in_element((By.ID, 'page_information_pt_1'), 'Page 1 of 280'))
        page_information_2 = self.page_wait.until(EC.text_to_be_present_in_element((By.ID, 'page_information_pt_2'), '(1-30 of 8388 items)'))

        self.assertTrue(page_information)
        self.assertTrue(page_information_2)

    def test_button_first_page(self):
        next_page_button = self.browser.find_element(By.ID, 'next_page_button')
        next_page_button.click()

        first_page_button = self.page_wait.until(EC.presence_of_element_located((By.ID, 'first_page_button')))
        first_page_button.click()
        
        page_information = self.page_wait.until(EC.text_to_be_present_in_element((By.ID, 'page_information_pt_1'), 'Page 1 of 33721'))
        page_information_2 = self.page_wait.until(EC.text_to_be_present_in_element((By.ID, 'page_information_pt_2'), '(1-30 of 1011616 items)'))

        self.assertTrue(page_information)
        self.assertTrue(page_information_2)

    def test_button_next_page(self):
        next_page_button = self.browser.find_element(By.ID, 'next_page_button')
        next_page_button.click()

        page_information = self.page_wait.until(EC.text_to_be_present_in_element((By.ID, 'page_information_pt_1'), 'Page 2 of 33721'))
        page_information_2 = self.page_wait.until(EC.text_to_be_present_in_element((By.ID, 'page_information_pt_2'), '(31-60 of 1011616 items)'))

        self.assertTrue(page_information)
        self.assertTrue(page_information_2)

    def test_button_last_page(self):
        last_page_button = self.browser.find_element(By.ID, 'last_page_button')
        last_page_button.click()
        
        page_information = self.page_wait.until(EC.text_to_be_present_in_element((By.ID, 'page_information_pt_1'), 'Page 33721 of 33721'))
        page_information_2 = self.page_wait.until(EC.text_to_be_present_in_element((By.ID, 'page_information_pt_2'), '(1011601-1011616 of 1011616 items)'))

        self.assertTrue(page_information)
        self.assertTrue(page_information_2)

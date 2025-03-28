import os
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ======================== CONFIGURATION ======================== #
class Config:
    BASE_URL = "https://automationexercise.com/"
    TIMEOUT = 20


# ======================== LOGGER SETUP ======================== #
logging.basicConfig(
    filename="test_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


# ======================== FIXTURE FOR DRIVER ======================== #
@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(Config.BASE_URL)
    driver.maximize_window()
    yield driver
    driver.quit()


# ======================== PAGE OBJECT MODEL ======================== #
class ProductsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.TIMEOUT)
        self.products_link = (By.XPATH, "//a[@href='/products']")
        self.header_text = (By.XPATH, "//h2[contains(text(), 'All Products')]")
        self.search_input = (By.XPATH, "//input[@id='search_product']")
        self.search_button = (By.XPATH, "//button[@id='submit_search']")
        self.search_results_header = (By.XPATH, "//h2[contains(text(), 'Searched Products')]")
        self.product_list = (By.XPATH, "//div[@class='productinfo text-center']/p")

    def navigate_to_products(self):
        self.wait.until(EC.element_to_be_clickable(self.products_link)).click()
        header_element = self.wait.until(EC.visibility_of_element_located(self.header_text))
        assert header_element.text.strip().upper() == "ALL PRODUCTS", "Navigation to 'All Products' page failed!"

    def search_product(self, product_name):
        self.wait.until(EC.visibility_of_element_located(self.search_input)).send_keys(product_name)
        self.wait.until(EC.element_to_be_clickable(self.search_button)).click()
        assert self.wait.until(EC.visibility_of_element_located(
            self.search_results_header)).is_displayed(), "Search results section not visible!"

    def verify_searched_products(self, search_term):
        product_elements = self.wait.until(EC.visibility_of_all_elements_located(self.product_list))
        assert len(product_elements) > 0, "No products found for the searched term!"
        for product in product_elements:
            assert search_term in product.text.lower(), f"Unrelated product found: {product.text}"


# ======================== TEST CASE ======================== #
def test_search_product(driver):
    logger.info("Search Product Test Started")
    product_page = ProductsPage(driver)
    product_page.navigate_to_products()
    product_page.search_product("women")
    product_page.verify_searched_products("women")
    logger.info("Search Product Test Passed")


# ======================== RUN TESTS ======================== #
if __name__ == "__main__":
    pytest.main(["--html=reports/test_report.html", "--self-contained-html", "-n 2"])
git init

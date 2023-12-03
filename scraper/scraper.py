import os
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from container import Container
from element import Element

N_SAVED_PHOTOS = 2


class Scraper:
    def __init__(self):
        options = Options()
        options.page_load_strategy = "normal"
        self._driver = webdriver.Firefox(options=options)

    def start(self, url):
        self._driver.get(url)
        self._iterate_categories()
        self._stop()

    def _iterate_categories(self):
        elements = self._driver.find_elements(
            By.CSS_SELECTOR,
            ".category-menu > div:nth-child(1) > ul > li > a:nth-child(1)",
        )

        categories = Container("categories")

        for element in elements:
            link = element.get_attribute("href")
            name = element.find_element(By.CSS_SELECTOR, "span:nth-child(1)").text

            category = Element(link)
            category.add_attribute("name", name)

            categories.add_element(category)

        categories.write()

        for category in categories.get_elements():
            self._iterate_subcategories(category)

    def _iterate_subcategories(self, category: Element):
        self._driver.get(category.get_link())

        elements = self._driver.find_elements(
            By.CSS_SELECTOR,
            ".sidebar-menu > li:nth-child(1) > ul:nth-child(2) > li:nth-child(1) > ul:nth-child(2) > li > a:nth-child(1)",
        )

        subcategories = Container("subcategories")

        for element in elements:
            link = element.get_attribute("href")
            name = element.find_element(By.CSS_SELECTOR, "span:nth-child(1)").text

            subcategory = Element(link)
            subcategory.add_attribute("name", name)
            subcategory.add_attribute("category", category.get_attribute("name"))

            subcategories.add_element(subcategory)

        subcategories.write()

        for subcategory in subcategories.get_elements():
            self._iterate_products(subcategory)

    def _iterate_products(self, subcategory: Element):
        self._driver.get(subcategory.get_link())

        elements = self._driver.find_elements(
            By.CSS_SELECTOR,
            ".listing h3 > a:nth-child(1)",
        )

        products = Container("prodcuts")

        for element in elements:
            link = element.get_attribute("href")
            product = Element(link)
            products.add_element(product)

        for product in products.get_elements():
            self._save_product_info(product, subcategory)

        products.write()

    def _save_product_info(self, product: Element, subcategory: Element):
        self._driver.get(product.get_link())

        name = self._driver.find_element(By.CSS_SELECTOR, "h1").text
        product.add_attribute("name", name)

        product.add_attribute("category", subcategory.get_attribute("category"))
        product.add_attribute("subcategory", subcategory.get_attribute("name"))

        try:
            price = self._driver.find_element(By.CSS_SELECTOR, ".price--large").text
            product.add_attribute("available", "yes")
            product.add_attribute("price", price)
        except NoSuchElementException:
            product.add_attribute("available", "no")
            product.add_attribute("price", -1)

        try:
            old_price = self._driver.find_element(
                By.CSS_SELECTOR, ".prices__price-old > div:nth-child(1)"
            ).text
            product.add_attribute("old_price", old_price)
        except NoSuchElementException:
            product.add_attribute("old_price", -1)

        self.save_product_photos(product)

    def save_product_photos(self, product: Element):
        elements = self._driver.find_elements(
            By.CSS_SELECTOR, ".c-gallery-screen-photo > img"
        )

        links = [element.get_attribute("src") for element in elements]

        saved_photos = 0
        pattern = re.compile(".*\.[^\/]*$")

        for id, link in enumerate(links):
            if not saved_photos < N_SAVED_PHOTOS:
                break

            if not pattern.match(link):
                continue

            self._driver.get(link)
            path = os.path.join("photos", f"{product.get_attribute('id')}_{id}.png")
            self._driver.save_screenshot(path)
            saved_photos += 1

    def _stop(self):
        self._driver.quit()

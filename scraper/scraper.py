import os
import random
import re

from minify_html import minify
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from container import Container
from element import Element
import tools

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

    def _get_product_weight(self):
        parameters = self._driver.find_elements(
            By.CSS_SELECTOR, ".product-parameters-content > .parameter-row"
        )

        for parameter in parameters:
            name = parameter.find_element(By.CSS_SELECTOR, ".parameter-name").text
            value = parameter.find_element(
                By.CSS_SELECTOR, ".parameter-description"
            ).text

            if name == "Waga [g]:":
                return tools.extract_digits(value).replace(",", ".")

        return random.uniform(1, 60)

    def _iterate_categories(self):
        elements = self._driver.find_elements(
            By.CSS_SELECTOR,
            ".category-menu > div:nth-child(1) > ul > li > a:nth-child(1)",
        )

        categories = Container("categories", "categories.csv")

        for element in elements:
            link = element.get_attribute("href")
            name = element.find_element(By.CSS_SELECTOR, "span:nth-child(1)").text

            category = Element(link)
            category.set_attribute("Active", 1)
            category.set_attribute("Name", name)
            category.set_attribute("Parent category", "Strona główna")
            category.set_attribute("Root category", 0)

            categories.add_element(category)

        categories.write_attributes()

        for category in categories:
            self._iterate_subcategories(category)

    def _iterate_subcategories(self, category: Element):
        self._driver.get(category.get_link())

        elements = self._driver.find_elements(
            By.CSS_SELECTOR,
            ".sidebar-menu > li:nth-child(1) > ul:nth-child(2) > li:nth-child(1) > ul:nth-child(2) > li > a:nth-child(1)",
        )

        subcategories = Container("subcategories", "categories.csv")

        for element in elements:
            link = element.get_attribute("href")
            name = element.find_element(By.CSS_SELECTOR, "span:nth-child(1)").text

            subcategory = Element(link)
            subcategory.set_attribute("Active", 1)
            subcategory.set_attribute("Name", name)

            parent_category_name = category.get_attribute("Name")
            subcategory.set_attribute("Parent category", parent_category_name)

            subcategory.set_attribute("Root category", 0)

            subcategories.add_element(subcategory)

        subcategories.write_attributes()

        for subcategory in subcategories:
            self._iterate_products(subcategory)

    def _iterate_products(self, subcategory: Element):
        self._driver.get(subcategory.get_link())

        elements = self._driver.find_elements(
            By.CSS_SELECTOR,
            ".listing h3 > a:nth-child(1)",
        )

        products = Container("prodcuts", "products.csv")

        for element in elements:
            link = element.get_attribute("href")
            product = Element(link)
            products.add_element(product)

        for product in products:
            self._save_product_info(product, subcategory)

        products.write_attributes()

    def _save_product_info(self, product: Element, subcategory: Element):
        self._driver.get(product.get_link())

        name = self._driver.find_element(By.CSS_SELECTOR, "h1").text
        name.replace("<", "&lt;").replace(">", "&gt;")
        product.set_attribute("Name", name)

        categories = f"{subcategory.get_attribute('Parent category')},{subcategory.get_attribute('Name')}"
        product.set_attribute("Categories", categories)

        try:
            price = self._driver.find_element(By.CSS_SELECTOR, ".price--large").text
            product.set_attribute("Active", 1)
            product.set_attribute("Price brutto", tools.extract_digits(price))
        except NoSuchElementException:
            product.set_attribute("Active", 0)
            product.set_attribute("Price brutto", 0)

        product.set_attribute("Weight", self._get_product_weight())
        product.set_attribute("Tax ID", 1)
        product.set_attribute("Quantity", random.randint(0, 120))

        description = self._driver.find_element(
            By.CSS_SELECTOR, ".product-description-content > .cms"
        ).get_attribute("innerHTML")
        description = re.sub(r"<[^>]+>", " ", minify(description))
        product.set_attribute("Description", description)

        self._save_product_photos(product)

    def _save_product_photos(self, product: Element):
        elements = self._driver.find_elements(
            By.CSS_SELECTOR, ".c-gallery-screen-photo > img"
        )

        links = [element.get_attribute("src") for element in elements]
        paths = ""

        saved_photos = 0
        pattern = re.compile(".*\.[^\/]*$")

        for id, link in enumerate(links):
            if not saved_photos < N_SAVED_PHOTOS:
                break

            if not pattern.match(link):
                continue

            self._driver.get(link)
            path = os.path.join("photos", f"{product.get_attribute('id')}_{id}.png")
            paths += f"http://localhost/{path},"
            self._driver.save_screenshot(path)
            saved_photos += 1

        product.set_attribute("Photo URLs", paths[:-1])

    def _stop(self):
        self._driver.quit()

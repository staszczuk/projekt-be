import csv
import os
from typing import List

from element import Element


class Container:
    overridden = []

    def __init__(self, name):
        self._name = name
        self._elements: List[Element] = []
        self._file_path = os.path.join("csv", name + ".csv")

    def add_element(self, element):
        self._elements.append(element)

    def get_elements(self):
        return self._elements

    def write(self):
        if not self._elements:
            return

        if self._file_path not in Container.overridden:
            with open(self._file_path, "w", buffering=1) as file:
                writer = csv.writer(file)
                attribute_names = self._elements[0].get_attribute_names()
                writer.writerow(attribute_names)

            Container.overridden.append(self._file_path)

        with open(self._file_path, "a", buffering=1) as file:
            writer = csv.writer(file)

            for element in self._elements:
                writer.writerow(element.get_attribute_values())

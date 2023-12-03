import csv
import os
from typing import List

from element import Element


class Container:
    overridden_files = []

    def __init__(self, name):
        self._name = name
        self._elements: List[Element] = []
        self._file_path = os.path.join("csv", name + ".csv")

    def __iter__(self):
        return iter(self._elements)

    def add_element(self, element):
        self._elements.append(element)

    def write_attributes(self):
        if not self._elements:
            return

        if self._file_path not in Container.overridden_files:
            self._write_attribute_names()
            Container.overridden_files.append(self._file_path)

        with open(self._file_path, "a", buffering=1) as file:
            writer = csv.writer(file)

            for element in self._elements:
                writer.writerow(element.get_attribute_values())

    def _write_attribute_names(self):
        with open(self._file_path, "w", buffering=1) as file:
            writer = csv.writer(file)
            names = self._elements[0].get_attribute_names()
            writer.writerow(names)

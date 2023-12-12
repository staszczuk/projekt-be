class Element:
    id = 0

    def __init__(self, link):
        self._link = link
        self._attributes = {"id": Element.id}
        Element.id += 1

    def get_attribute(self, name):
        return self._attributes.get(name)

    def get_attribute_names(self):
        return self._attributes.keys()

    def get_attribute_values(self):
        return self._attributes.values()

    def get_link(self):
        return self._link

    def set_attribute(self, name, value):
        self._attributes.update({name: value})

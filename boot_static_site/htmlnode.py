
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        if value is None and children is None:
            raise ValueError("value and children cannot both be None")
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        prop_string = ""
        for key, value in self.props.items():
            prop_string += f" {key}=\"{value}\""
        return prop_string[1:]

    def display_children(self):
        if self.children is None:
            return ""
        children_string = ""
        for child in self.children:
            children_string +=  str(child) + "\n"
        return children_string

    def __repr__(self):
        return f"tag: {self.tag}\n" \
               f"value: {self.value}\n" \
               f"children:\n{self.display_children()}\n" \
               f"props: {self.props_to_html()}"

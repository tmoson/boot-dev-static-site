from .htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("Value required for leaf node")
        if isinstance(tag, list) or isinstance(value, list) or isinstance(props, list):
            raise ValueError("No children permitted for child nodes")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag} {super().props_to_html()}>{self.value}</{self.tag}>"

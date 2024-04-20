from .htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if children is None or children == []:
            raise ValueError("Children required for parent node")
        if not isinstance(tag, list) and not isinstance(children, list) and not isinstance(props, list):
            raise ValueError("Children required for parent nodes")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag required for HTML conversion")
        html = f"<{self.tag}"
        if self.props is None:
            html += ">"
        else:
            html += f" {super().props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        return html + f"</{self.tag}>"

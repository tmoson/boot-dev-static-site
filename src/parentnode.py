from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("tag required for parent node")
        elif children is None:
            raise ValueError("children required for parent node")
        if not isinstance(children, list):
            raise ValueError("value not supported for parent node")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag required for parent node")
        elif self.children is None:
            raise ValueError("children required for parent node")
        if self.props is None:
            html = f"<{self.tag}>"
            for child in self.children:
                html += f"{child.to_html()}"
            return html + f"</{self.tag}>"
        else:
            html = f"<{self.tag} {self.props_to_html()}>"
            for child in self.children:
                html += f"{child.to_html()}"
            return html + f"</{self.tag}>"


class TextNode:

    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url

    def eq(self, node):
        return (self.text == node.text and
                self.text_type == node.text_type and
                self.url == node.url)

    def repr(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

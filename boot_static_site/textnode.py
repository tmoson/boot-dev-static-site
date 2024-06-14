import re


class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def eq(self, node):
        return (self.text == node.text and
                self.text_type == node.text_type and
                self.url == node.url)

    def split_nodes_delimiter(nodes, delimiter, text_type):
        split_nodes = []
        for node in nodes:
            split_text = node.text.split(delimiter)
            num_nodes = len(split_text)
            if num_nodes % 2 == 0 and num_nodes != 0:
                raise Exception("ERROR: missing delimiter")
            for i in range(0, len(split_text)):
                if i % 2 == 0:
                    split_nodes.append(TextNode(split_text[i], node.text_type))
                else:
                    split_nodes.append(TextNode(split_text[i], text_type))
        return split_nodes

    def extract_markdown_images(text):
        return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    def extract_markdown_links(text):
        return re.findall(r"\[(.*?)\]\((.*?)\)", text)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

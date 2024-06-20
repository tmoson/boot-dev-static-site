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
                    split_nodes.append(TextNode(split_text[i], node.text_type, node.url))
                else:
                    split_nodes.append(TextNode(split_text[i], text_type, node.url))
        return split_nodes

    def extract_markdown_images(text):
        return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    def extract_markdown_links(text):
        return re.findall(r"\[(.*?)\]\((.*?)\)", text)

    def split_nodes_images(nodes):
        split_nodes = []
        for node in nodes:
            if node.text_type == "link" or node.text_type == "image":
                split_nodes.append(node)
                continue
            links = re.findall(r"!\[(.*?)\]\((.*?)\)", node.text)
            if len(links) == 0:
                split_nodes.append(node)
                continue
            split_text = list(filter(None, node.text.split(f"![{links[0][0]}]({links[0][1]})", 1)))
            link_at_start = re.match(r"^!\[(.*?)\]\((.*?)\)", node.text) is not None
            for i in range(0, len(links)):
                if link_at_start:
                    split_nodes.append(TextNode(text=links[i][0], text_type='image', url=links[i][1]))
                    split_nodes.append(TextNode(split_text[0], "text"))
                else:
                    split_nodes.append(TextNode(split_text[0], "text"))
                    split_nodes.append(TextNode(text=links[i][0], text_type='image', url=links[i][1]))
                if i < len(links) - 1:
                    link_at_start = re.match(r"^!\[(.*?)\]\((.*?)\)", split_text[1]) is not None
                    split_text = list(filter(None, split_text[1].split(f"![{links[i+1][0]}]({links[i+1][1]})", 1)))
                elif len(split_text) > 1:
                    split_nodes.append(TextNode(split_text[1], "text"))
        return split_nodes

    def split_nodes_links(nodes):
        split_nodes = []
        for node in nodes:
            if node.text_type == "link" or node.text_type == "image":
                split_nodes.append(node)
                continue
            links = re.findall(r"\[(.*?)\]\((.*?)\)", node.text)
            if len(links) == 0:
                split_nodes.append(node)
                continue
            split_text = list(filter(None, node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)))
            link_at_start = re.match(r"^\[(.*?)\]\((.*?)\)", node.text) is not None
            for i in range(0, len(links)):
                if link_at_start:
                    split_nodes.append(TextNode(text=links[i][0], text_type='link', url=links[i][1]))
                    split_nodes.append(TextNode(split_text[0], "text"))
                else:
                    split_nodes.append(TextNode(split_text[0], "text"))
                    split_nodes.append(TextNode(text=links[i][0], text_type='link', url=links[i][1]))
                if i < len(links) - 1:
                    link_at_start = re.match(r"^\[(.*?)\]\((.*?)\)", split_text[1]) is not None
                    split_text = list(filter(None, split_text[1].split(f"[{links[i+1][0]}]({links[i+1][1]})", 1)))
                elif len(split_text) > 1:
                    split_nodes.append(TextNode(split_text[1], "text"))
        return split_nodes

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_to_textnodes(text):
    initial_node = TextNode(text, "text")
    return TextNode.split_nodes_delimiter(
              TextNode.split_nodes_delimiter(
                TextNode.split_nodes_delimiter(
                    TextNode.split_nodes_links(TextNode.split_nodes_images([initial_node])),
                "**", "bold"),
              "*", "italic"),
           "`", "code")

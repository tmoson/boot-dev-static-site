from textnode import TextNode, TextType
from leafnode import LeafNode
import re

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            return LeafNode(tag=None, value=text_node.text)
    return None

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        split_nodes = str.split(node.text, delimiter)
        start_ind = 0
        num_nodes = len(split_nodes)
        if split_nodes[start_ind] == '':
            ++start_ind
        if num_nodes % 2 == 0 and num_nodes != 0:
            raise Exception("ERROR: missing delimiter")
        for i in range(start_ind, num_nodes):
            if i % 2 == 0:
                if split_nodes[i] == '':
                    continue
                else:
                    new_nodes.append(TextNode(split_nodes[i], node.text_type))
            else:
                new_nodes.append(TextNode(split_nodes[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def main():
    test_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(test_node)

main()

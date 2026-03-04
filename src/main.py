from nodefunctions import markdown_to_html_node
from textnode import TextNode, TextType


def main():
    test_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(test_node)


main()

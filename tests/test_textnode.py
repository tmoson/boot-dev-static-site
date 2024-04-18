import pytest

from boot_static_site.textnode import TextNode

class TestTextNode():
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        assert node.eq(node2)

    def test_creation(self):
        node = TextNode("This is a text node", "bold")
        assert node.repr() == "TextNode(This is a text node, bold, None)"

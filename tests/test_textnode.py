import pytest

from boot_static_site.textnode import TextNode

class TestTextNode():
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        assert node.eq(node2)

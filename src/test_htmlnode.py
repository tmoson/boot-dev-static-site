import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="div", value="This is some text", props={"class": "body", "href": "https://www.boot.dev"})
        self.assertEqual(
            node.props_to_html(),
            "class=\"body\" href=\"https://www.boot.dev\""
        )

    def test_contents(self):
        node = HTMLNode(tag="p", value="This is some text", props={"class": "body"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is some text")
        self.assertEqual(node.props, {"class": "body"})
        node2 = HTMLNode(tag="div", children=[node])
        self.assertEqual(node2.tag, "div")
        self.assertEqual(len(node2.children), 1)
        self.assertEqual(node2.children[0], node)

    def test_repr(self):
        node = HTMLNode(tag="div", value="This is some text", props={"class": "body", "href": "https://www.boot.dev"})
        self.assertEqual(node.__repr__(), "HTMLNode(div, This is some text, None, {'class': 'body', 'href': 'https://www.boot.dev'})")

import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_init_and_to_html(self):
        leaf_node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            leaf_node1.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )
        leaf_node2 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf_node2.to_html(), "<p>This is a paragraph of text.</p>")

    def test_require_value(self):
        with self.assertRaises(ValueError):
            bad_node = LeafNode("a", None, {"text": "some value"})

    def test_no_children(self):
        with self.assertRaises(ValueError):
            good_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
            bad_node = LeafNode("p", "some text", [good_node])

import unittest
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        test_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode("a", "link text", {"href": "https://boot.dev"}),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"class": "test"},
        )
        self.assertEqual(
            test_node.to_html(),
            '<p class="test"><b>Bold text</b><a href="https://boot.dev">link text</a><i>italic text</i>Normal text</p>',
        )

    def test_to_html_with_granchild_props(self):
        grandchild_node = LeafNode("b", "grandchild", {"class": "special"})
        child_node = ParentNode("span", [grandchild_node], {"style": "unique"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span style="unique"><b class="special">grandchild</b></span></div>',
        )

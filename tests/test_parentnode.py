import pytest

from boot_static_site.leafnode import LeafNode
from boot_static_site.parentnode import ParentNode

class TestParentNode:
    def test_init_and_to_html(self):
        node = ParentNode(
            "p",
            [
             LeafNode("b", "Bold text"),
             LeafNode(None, "Normal text"),
             LeafNode("i", "italic text"),
             LeafNode(None, "Normal text"),
            ],
        )
        assert node.to_html() == '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        node.props = {"class": "p1"}
        assert node.to_html() == '<p class="p1"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'

    def test_nested_parents(self):
        node = ParentNode(
            "p",
            [
             LeafNode("b", "Bold text"),
             LeafNode(None, "Normal text"),
             LeafNode("i", "italic text"),
             LeafNode(None, "Normal text"),
            ],
        )
        double_parent = ParentNode(
            "html",
            [
             LeafNode("h1", "Header Text", {"class": "main-header"}),
             node,
             LeafNode("p", "Closing Text")
            ],
        )
        html = '<html><h1 class="main-header">Header Text</h1><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p>Closing Text</p></html>'
        assert double_parent.to_html() == html
        
    def test_bad_init(self):
        with pytest.raises(ValueError) as excinfo:
            bad_node = ParentNode("p", None)
        with pytest.raises(ValueError) as excinfo:
            bad_node_2 = ParentNode(None, "Oops, this is how leaf nodes are created", None)

    def test_no_tag_html(self):
        with pytest.raises(ValueError) as excinfo:
            no_tag_parent = ParentNode(
                None,
                [
                 LeafNode("b", "Bold text"),
                 LeafNode(None, "Normal text"),
                 LeafNode("i", "italic text"),
                 LeafNode(None, "Normal text"),
                ],
            )
            no_tag_parent.to_html()

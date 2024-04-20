import pytest

from boot_static_site.leafnode import LeafNode

class TestLeafNode:
    def test_init_and_to_html(self):
        leaf_node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        assert leaf_node1.to_html() == '<a href="https://www.google.com">Click me!</a>'
        leaf_node2 = LeafNode("p", "This is a paragraph of text.")
        assert leaf_node2.to_html() == '<p>This is a paragraph of text.</p>'

    def test_require_value(self):
        with pytest.raises(ValueError) as excinfo:
            bad_node = LeafNode("a", None, {"text": "some value"})

    def test_no_children(self):
        with pytest.raises(ValueError) as excinfo:
            leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
            bad_node = LeafNode("p", "Some text", [leaf_node])

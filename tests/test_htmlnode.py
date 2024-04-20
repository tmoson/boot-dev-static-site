import pytest

from boot_static_site.htmlnode import HTMLNode

class TestHTMLNode:
    def test_init_and_to_string(self):
        node_1 = HTMLNode(tag="h1", value="This is a header node", props={"class": "top-header"})
        node_1_string = "tag: h1\n" \
                        "value: This is a header node\n" \
                        "children:\n\n" \
                        "props: class=\"top-header\""
        assert str(node_1) == node_1_string
        node_2 = HTMLNode(tag="h2", value="subheader", children=[node_1], props={"href": "https://www.boot.dev"})
        assert str(node_2) == "tag: h2\n" \
                              "value: subheader\n" \
                              f"children:\n{node_1_string}\n\n" \
                              "props: href=\"https://www.boot.dev\""

    def test_init_exception(self):
        with pytest.raises(ValueError) as excinfo:
            bad_node = HTMLNode(tag="h1", props={"href": "https://www.boot.dev"})

    def test_props_to_string(self):
        node = HTMLNode(tag="h1", value="here to create a proper node", props={"class": "top-header", "href": "https://www.boot.dev", "style": "bold"})
        assert node.props_to_html() == 'class="top-header" href="https://www.boot.dev" style="bold"'
        
    

import pytest

from boot_static_site.textnode import TextNode

class TestTextNode():
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        assert node.eq(node2)

    def test_creation(self):
        node = TextNode("This is a text node", "bold")
        assert str(node) == "TextNode(This is a text node, bold, None)"
        node.url = "https://www.boot.dev"
        assert str(node) == "TextNode(This is a text node, bold, https://www.boot.dev)"
        node = TextNode("This is a new node", "bold", "https://www.boot.dev")
        assert str(node) == "TextNode(This is a new node, bold, https://www.boot.dev)"


    def test_split_nodes(self):
        single_node = TextNode("This is text with a `code block` word", "text")
        expected_split_nodes = [
            TextNode("This is text with a ", "text", None),
            TextNode("code block", "code", None),
            TextNode(" word", "text", None)
        ]
        split_nodes = TextNode.split_nodes_delimiter([single_node], "`", "code")
        assert len(split_nodes) == len(expected_split_nodes)
        for i in range(0, len(expected_split_nodes)):
            assert str(split_nodes[i]) == str(expected_split_nodes[i])

    def test_split_nodes_nested(self):
        node_1 = TextNode("This is text with a `code block` word", "text")
        node_2 = TextNode("This is a second node with another `code block` and a secondary **bold text block** for nested testing", "text")
        new_nodes_expected = [
            TextNode("This is text with a ", "text", None),
            TextNode("code block", "code", None),
            TextNode(" word", "text", None),
            TextNode("This is a second node with another ", "text", None),
            TextNode("code block", "code", None),
            TextNode(" and a secondary **bold text block** for nested testing", "text", None)
        ]
        new_nodes_1 = TextNode.split_nodes_delimiter([node_1, node_2], "`", "code")
        assert len(new_nodes_1) == len(new_nodes_expected)
        for i in range(0, len(new_nodes_expected)):
            assert str(new_nodes_1[i]) == str(new_nodes_expected[i])
        new_nodes_2 = TextNode.split_nodes_delimiter(new_nodes_1, "**", "bold")
        new_nodes_expected_2 = [
            TextNode("This is text with a ", "text", None),
            TextNode("code block", "code", None),
            TextNode(" word", "text", None),
            TextNode("This is a second node with another ", "text", None),
            TextNode("code block", "code", None),
            TextNode(" and a secondary ", "text", None),
            TextNode("bold text block", "bold", None),
            TextNode(" for nested testing", "text", None)
        ]
        assert len(new_nodes_2) == len(new_nodes_expected_2)
        for i in range(0, len(new_nodes_expected)):
            assert str(new_nodes_2[i]) == str(new_nodes_expected_2[i])
        node_3 = TextNode("This is a 3rd text node that uses *italics* for *emphasis*.", "text")
        new_nodes_3 = TextNode.split_nodes_delimiter(TextNode.split_nodes_delimiter(TextNode.split_nodes_delimiter([node_1, node_2, node_3], "`", "code"), "**", "bold"), "*", "italics")
        new_nodes_expected_3 = [
            TextNode("This is text with a ", "text", None),
            TextNode("code block", "code", None),
            TextNode(" word", "text", None),
            TextNode("This is a second node with another ", "text", None),
            TextNode("code block", "code", None),
            TextNode(" and a secondary ", "text", None),
            TextNode("bold text block", "bold", None),
            TextNode(" for nested testing", "text", None),
            TextNode("This is a 3rd text node that uses ", "text", None),
            TextNode("italics", "italics", None),
            TextNode(" for ", "text", None),
            TextNode("emphasis", "italics", None),
            TextNode(".", "text", None)
        ]
        
        assert len(new_nodes_3) == len(new_nodes_expected_3)
        for i in range(0, len(new_nodes_expected)):
            assert str(new_nodes_3[i]) == str(new_nodes_expected_3[i])

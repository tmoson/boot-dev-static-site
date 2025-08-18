import unittest
from textnode import TextNode, TextType
from main import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_example(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(expected, new_nodes)

    def test_bold(self):
        node = TextNode("This is text with **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(expected, new_nodes)

    def test_italics(self):
        node = TextNode("This is a text node with *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is a text node with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(expected, new_nodes)

    def test_blah(self):
        self.assertEqual(1, 1)

    def test_nested(self):
        node = TextNode("This is text with both **bolded text** and a `code block`", TextType.TEXT)
        first_node_group = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_first_group = [
            TextNode("This is text with both **bolded text** and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE)
        ]
        self.assertEqual(expected_first_group, first_node_group)
        second_node_group = split_nodes_delimiter(first_node_group, "**", TextType.BOLD)
        expected_second_group = [
            TextNode("This is text with both ", TextType.TEXT),
            TextNode("bolded text", TextType.BOLD),
            TextNode(" and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE)
        ]
        self.assertEqual(expected_second_group, second_node_group)

    def test_starting_split(self):
        node = TextNode("**starting with bold text** shouldn't be an issue", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("starting with bold text", TextType.BOLD),
            TextNode(" shouldn't be an issue", TextType.TEXT)
        ]
        self.assertEqual(expected, new_nodes)

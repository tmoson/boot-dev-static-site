import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_type_neq(self):
        node = TextNode("This is text", TextType.BOLD)
        node2 = TextNode("This is text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_link(self):
        link = TextNode("describing text", TextType.LINK, "https://www.boot.dev")
        link2 = TextNode("describing text", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(
            link, link2
        )  # check that the value in the url portion is checked
        link2 = TextNode(
            "this is different text", TextType.LINK, "https://www.boot.dev"
        )
        self.assertNotEqual(link, link2)  # make sure text content is checked

    def test_image(self):
        link = TextNode("describing text", TextType.LINK, "https://www.boot.dev")
        image = TextNode("describing text", TextType.IMAGE, "/path/to/image.png")
        self.assertNotEqual(link, image)  # check that an image can't be confused for a
        image2 = TextNode(
            "describing text", TextType.IMAGE, "/path/to/separate_image.png"
        )
        self.assertNotEqual(
            image, image2
        )  # check that url for images is treated the same as links
        image2 = TextNode(
            "this is different describing text", TextType.IMAGE, "/path/to/image.png"
        )
        self.assertNotEqual(
            image, image2
        )  # make sure that text must be the same for equality

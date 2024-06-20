import pytest

from boot_static_site.textnode import TextNode, text_to_textnodes

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

    def test_extract_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        extracted_img_links = TextNode.extract_markdown_images(text)
        expected_img_links = [
            ('image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png'),
            ('another', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png')
        ]
        assert len(extracted_img_links) == len(expected_img_links)
        for i in range(0, len(extracted_img_links)):
            assert len(extracted_img_links[i]) == 2
            assert extracted_img_links[i][0] == expected_img_links[i][0]
            assert extracted_img_links[i][1] == expected_img_links[i][1]
        no_img_text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        assert TextNode.extract_markdown_images(no_img_text) == []

    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        extracted_links = TextNode.extract_markdown_links(text)
        expected_links = [
            ('link', 'https://www.example.com'),
            ('another', 'https://www.example.com/another')
        ]
        assert len(extracted_links) == len(expected_links)
        for i in range(0, len(extracted_links)):
            assert len(extracted_links[i]) == 2
            assert extracted_links[i][0] == expected_links[i][0]
            assert extracted_links[i][1] == expected_links[i][1]

    def test_split_nodes_images(self):
        node1 = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text")
        node2 = TextNode("Another node that ends with ![another image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)", "text")
        node3 = TextNode("![An image](https://www.somedomain.com/imgs/abc123.png) at the beginning.", "text")
        expected_nodes = [
            TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", "text"),
            TextNode("second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png")
        ]
        actual_nodes = TextNode.split_nodes_images([node1])
        assert len(actual_nodes) == len(expected_nodes)
        for i in range(0, len(actual_nodes)):
            assert str(actual_nodes[i]) == str(expected_nodes[i])
        actual_nodes.append(node2)
        actual_nodes.append(node3)
        expected_nodes = [
            TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", "text"),
            TextNode("second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
            TextNode("Another node that ends with ", "text"),
            TextNode("another image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode("An image", "image", "https://www.somedomain.com/imgs/abc123.png"),
            TextNode(" at the beginning.", "text")
        ]
        actual_nodes = TextNode.split_nodes_images(actual_nodes)
        assert len(actual_nodes) == len(expected_nodes)
        for i in range(0, len(actual_nodes)):
            assert str(actual_nodes[i]) == str(expected_nodes[i])
        
        
            
    def test_split_nodes_links(self):
        node1 = TextNode("This is text with a [link](https://www.example.com) and [another](https://www.example.com/another) link with some more text after it.", "text")
        node2 = TextNode("This is a separate node that has a link as the final part of the string, [like so](https://www.google.com)", "text")
        node3 = TextNode("[A starting link](https://www.example.com/start) to test that nodes starting with a link work", "text")
        expected_nodes = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "https://www.example.com"),
            TextNode(" and ", "text"),
            TextNode("another", "link", "https://www.example.com/another"),
            TextNode(" link with some more text after it.", "text")
        ]
        actual_nodes = TextNode.split_nodes_links([node1])
        assert len(actual_nodes) == len(expected_nodes)
        for i in range(0, len(actual_nodes)):
            assert str(actual_nodes[i]) == str(expected_nodes[i])
        actual_nodes.append(node2)
        expected_nodes = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "https://www.example.com"),
            TextNode(" and ", "text"),
            TextNode("another", "link", "https://www.example.com/another"),
            TextNode(" link with some more text after it.", "text"),
            TextNode("This is a separate node that has a link as the final part of the string, ", "text"),
            TextNode("like so", "link", "https://www.google.com")
        ]
        actual_nodes = TextNode.split_nodes_links(actual_nodes)
        assert len(actual_nodes) == len(expected_nodes)
        for i in range(0, len(actual_nodes)):
            assert str(actual_nodes[i]) == str(expected_nodes[i])
        actual_nodes.append(node3)
        expected_nodes = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "https://www.example.com"),
            TextNode(" and ", "text"),
            TextNode("another", "link", "https://www.example.com/another"),
            TextNode(" link with some more text after it.", "text"),
            TextNode("This is a separate node that has a link as the final part of the string, ", "text"),
            TextNode("like so", "link", "https://www.google.com"),
            TextNode("A starting link", "link", "https://www.example.com/start"),
            TextNode(" to test that nodes starting with a link work", "text")
        ]
        actual_nodes = TextNode.split_nodes_links(actual_nodes)
        assert len(actual_nodes) == len(expected_nodes)
        for i in range(0, len(actual_nodes)):
            assert str(actual_nodes[i]) == str(expected_nodes[i])

    def test_text_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev")
        ]
        assert len(nodes) == len(expected)
        for i in range(0, len(nodes)):
            assert str(nodes[i]) == str(expected[i])
            

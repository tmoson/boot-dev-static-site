import pytest

from boot_static_site.blockmarkdown import markdown_to_blocks

class TestBlockMarkdown:
    def test_markdown_to_blocks(self):
        text = ("# This is a heading   "
                "\n"
                "\n"
                "  This is a paragraph of text. It has some **bold** and *italic* wordsd inside of it.\n"
                "\n"
                "* This is a list item  \n"
                "* This is another list item")
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* wordsd inside of it.",
            "* This is a list item\n* This is another list item"
        ]
        actual = markdown_to_blocks(text)
        assert len(actual) == len(expected)
        for i in range(0, len(actual)):
            assert actual[i] == expected[i]
        text = ("This is a **bolded** paragraph\n"
                "\n"
                "This is another paragraph with *italic* text and `code` here\n"
                "This is the same paragraph on a new line\n"
                "\n"
                "* This is a list\n"
                "* with items")
        expected = [
            "This is a **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]
        actual = markdown_to_blocks(text)
        assert len(actual) == len(expected)
        for i in range(0, len(actual)):
            assert actual[i] == expected[i]

import pytest

from boot_static_site.blockmarkdown import (
    type_heading,
    type_code,
    type_ordered_list,
    type_unordered_list,
    type_quote,
    type_paragraph,
    block_to_block_type,
    markdown_to_blocks
)

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

    def test_block_to_block_type(self):
        text = ("# This is a heading   "
                "\n"
                "\n"
                "  This is a paragraph of text. It has some **bold** and *italic* wordsd inside of it.\n"
                "\n"
                "* This is a list item  \n"
                "* This is another list item")
        blocks = markdown_to_blocks(text)
        expected = [ type_heading, type_paragraph, type_unordered_list ]
        for i in range(0, len(blocks)):
            assert block_to_block_type(blocks[i]) == expected[i]
        text = ("This is a **bolded** paragraph\n"
                "\n"
                "This is another paragraph with *italic* text and `code` here\n"
                "This is the same paragraph on a new line\n"
                "\n"
                "* This is a list\n"
                "* with items")
        blocks = markdown_to_blocks(text)
        expected = [ type_paragraph, type_paragraph, type_unordered_list ]
        for i in range(0, len(blocks)):
            assert block_to_block_type(blocks[i]) == expected[i]

    def test_block_to_block_type_quote(self):
        text = ("This is a paragraph\n"
                "\n"
                "This is another paragraph\n"
                "\n"
                "> This is the beginning of a blockquote\n"
                "> This is the second line of said quote\n"
                "> Here is the final line\n"
                "\n"
                "# We're adding a header here now")
        blocks = markdown_to_blocks(text)
        expected = [ type_paragraph, type_paragraph, type_quote, type_heading ]
        for i in range(0, len(blocks)):
            assert block_to_block_type(blocks[i]) == expected[i]
        text = ("This is a paragraph\n"
                "\n"
                "This is another paragraph\n"
                "\n"
                "> This is the beginning of a blockquote\n"
                "oops, I forgot a '>' at the start of this line\n"
                "> Here is the final line\n"
                "\n"
                "# We're adding a header here now")
        blocks = markdown_to_blocks(text)
        expected = [ type_paragraph, type_paragraph, type_paragraph, type_heading ]
        for i in range(0, len(blocks)):
            assert block_to_block_type(blocks[i]) == expected[i]
        

    def test_block_to_block_type_unordered_list(self):
        text = ("some text to start\n"
                "\n"
                "* a reasonable list item\n"
                "* see that I'm being consistent with my bullets\n"
                "\n"
                "# That mean's I'll have a nice unordered list")
        blocks = markdown_to_blocks(text)
        expected = [ type_paragraph, type_unordered_list, type_heading ]
        for i in range(0, len(blocks)):
            assert block_to_block_type(blocks[i]) == expected[i]
        text = ("some text to start\n"
                "\n"
                "- a reasonable list item\n"
                "- see that I'm being consistent with my bullets\n"
                "- Testing with '-' now to be sure both bullets work\n"
                "\n"
                "# That mean's I'll have a nice unordered list")
        blocks = markdown_to_blocks(text)
        expected = [ type_paragraph, type_unordered_list, type_heading ]
        for i in range(0, len(blocks)):
            assert block_to_block_type(blocks[i]) == expected[i]
        text = ("some text to start\n"
                "\n"
                "- a reasonable list item\n"
                "* I'm being inconsistent now. this isn't the way to make a list\n"
                "- This is going to just be a paragraph now\n"
                "\n"
                "# But this will still be a heading")
        blocks = markdown_to_blocks(text)
        expected = [ type_paragraph, type_paragraph, type_heading ]
        for i in range(0, len(blocks)):
            assert block_to_block_type(blocks[i]) == expected[i]
        text = ("some text to start\n"
                "\n"
                "- a reasonable list item\n"
                "-This is going to just be a paragraph now\n"
                "\n"
                "# But this will still be a heading")
        blocks = markdown_to_blocks(text)
        expected = [ type_paragraph, type_paragraph, type_heading ]
        for i in range(0, len(blocks)):
            assert block_to_block_type(blocks[i]) == expected[i]

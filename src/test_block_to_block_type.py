import unittest
from blocks import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_header(self):
        block = "### This is a normal header block"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
        bad_header = "####### This is a header with too many '#' characters"
        block_type = block_to_block_type(bad_header)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_code_block(self):
        block = """```
print(\"Hello World\")
```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
        bad_code = """```print(\"Hello World\")
```"""
        block_type = block_to_block_type(bad_code)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_quote(self):
        block = "> This is a thoughtful quote by someone"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_lists(self):
        u_list = """- some item of note
- another item of note
- last item"""
        block_type = block_to_block_type(u_list)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
        bad_u_list = """- first item
saying words blah blah blah
- some item"""
        block_type = block_to_block_type(bad_u_list)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        o_list = """1. numbered item
2. another item
3. third thing"""
        block_type = block_to_block_type(o_list)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
        bad_o_list = """1. numbered item
- I've screwed up my list types
3. third thing"""
        block_type = block_to_block_type(bad_o_list)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_default_assignment(self):
        block = """
This is just some normal text.
It has multiple lines, but meets none of the requirements for other types.
So it should register as just a paragraph"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

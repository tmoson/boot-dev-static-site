import unittest
from nodefunctions import extract_title


class TestExtractMDTitle(unittest.TestCase):
    def test_good_md(self):
        md = """
# this is a simple header

## this is another header

this is normal text"""
        title = extract_title(md)
        self.assertEqual(title, "this is a simple header")

    def test_multiple_h1_titles(self):
        md = """
this is some preamble, because sometimes you do that

# this is a simple header

now I'm moving on to more text
        
# this is another header that would use the h1 header, but we don't want it as our title!

this is normal text"""
        title = extract_title(md)
        self.assertEqual(title, "this is a simple header")

    def test_no_header(self):
        md = """
we're just using some text.

## I don't like h1 headers

* here
* is
* a
* list

this is normal text"""
        with self.assertRaises(ValueError):
            extract_title(md)

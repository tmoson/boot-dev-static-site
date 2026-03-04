import unittest
from nodefunctions import markdown_to_html_node


class TestMDToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_ordered_list(self):
        md = """
Here we have a list:

1. it's an ordered list
2. so we should have multiple items
3. that are numbered
4. but
5. we
6. have
7. to
8. check
9. that
10. multiple
11. digits
12. work
"""
        self.maxDiff = None
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Here we have a list:</p><ol><li>it's an ordered list</li><li>so we should have multiple items</li><li>that are numbered</li><li>but</li><li>we</li><li>have</li><li>to</li><li>check</li><li>that</li><li>multiple</li><li>digits</li><li>work</li></ol></div>",
        )

    def test_unordered_list(self):
        md = """
Now we have an unordered list:

- This is just a bunch of bullet points
- we don't need numbers
- but let's not forget that there can be [links](https://boot.dev)
- and then there's still other bullets to hit
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Now we have an unordered list:</p><ul><li>This is just a bunch of bullet points</li><li>we don't need numbers</li><li>but let's not forget that there can be <a href=\"https://boot.dev\">links</a></li><li>and then there's still other bullets to hit</li></ul></div>",
        )

    def test_headers(self):
        md = """
# This is just a normal header

then there's some text under it

## This is going to be an h2 header

### This is going to be an h3 header

#### This is going to be an **h4** header

##### This is going to be an _h5_ header

###### This is going to be an h6 header

####### This is going to end up being a normal paragraph!
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            "<div><h1>This is just a normal header</h1><p>then there's some text under it</p><h2>This is going to be an h2 header</h2><h3>This is going to be an h3 header</h3><h4>This is going to be an <b>h4</b> header</h4><h5>This is going to be an <i>h5</i> header</h5><h6>This is going to be an h6 header</h6><p>####### This is going to end up being a normal paragraph!</p></div>",
        )

    def test_block_quote(self):
        md = """
This is just a normal paragraph, but I'd like to quote **someone** from _publication_:

> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus efficitur massa elit, eu congue ante viverra et. Integer id malesuada eros. **Cras placerat id nibh a interdum.** Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.

Isn't that fascinating?
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            "<div><p>This is just a normal paragraph, but I'd like to quote <b>someone</b> from <i>publication</i>:</p><blockquote>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus efficitur massa elit, eu congue ante viverra et. Integer id malesuada eros. <b>Cras placerat id nibh a interdum.</b> Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.</blockquote><p>Isn't that fascinating?</p></div>",
        )

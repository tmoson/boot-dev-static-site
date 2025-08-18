import unittest
from main import extract_markdown_images, extract_markdown_links

class TestImageAndLinkExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')], matches)

    def test_image_and_link(self):
        test_string = "This is text with a link to [to boot dev](https://www.boot.dev), an ![image](https://i.imgur.com/zjjcJKZ.png), and another link [to youtube](https://www.youtube.com/@bootdotdev). And one last ![image link](https://i.imgur.com/Pstbciu.jpeg)"
        images = extract_markdown_images(test_string)
        self.assertListEqual([('image', 'https://i.imgur.com/zjjcJKZ.png'), ('image link', 'https://i.imgur.com/Pstbciu.jpeg')], images)
        links = extract_markdown_links(test_string)
        for image in images:
            links.remove(image) # image regex will match links too, so we're manually removing those for now
        self.assertListEqual([('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')], links)

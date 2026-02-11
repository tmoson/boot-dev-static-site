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
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_bad_extractions(self):
        bad_images = [
            "This is text with just a [link](https://www.boot.dev), but not an image link",
            "This is text with a bad ![image(https://i.imgur.com/zjjcJKZ.png)",
            "This is another bad !image(/path/to/png) reference.",
            "This has one last missing ![element](https://i.imgur.com/zjjcJKZ.png",
        ]
        for image_text in bad_images:
            self.assertListEqual([], extract_markdown_images(image_text))
        bad_links = [
            "This is a bad [link(https://www.boot.dev)",
            "I just want to link to [(https://google.com)]",
            "linking is broader than images like this(https://youtube.com)",
        ]
        for link_text in bad_links:
            self.assertEqual([], extract_markdown_links(link_text))
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            extract_markdown_links(
                "This is an ![image](https://i.imgur.com/zjjcJKZ.png)"
            ),
        )

    def test_image_and_link(self):
        test_string = "This is text with a link to [to boot dev](https://www.boot.dev), an ![image](https://i.imgur.com/zjjcJKZ.png), and another link [to youtube](https://www.youtube.com/@bootdotdev). And one last ![image link](https://i.imgur.com/Pstbciu.jpeg)"
        images = extract_markdown_images(test_string)
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("image link", "https://i.imgur.com/Pstbciu.jpeg"),
            ],
            images,
        )
        links = extract_markdown_links(test_string)
        for image in images:
            links.remove(
                image
            )  # image regex will match links too, so we're manually removing those for now
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            links,
        )

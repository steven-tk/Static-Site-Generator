import unittest

from nodesplit import extract_markdown_images, extract_markdown_links


class RegexExtraction(unittest.TestCase):


    # ====================
    # Image extraction tests
    # ====================

    def test_single_image(self):
        text = "This is ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "Here ![first](url1) and ![second](url2)"
        expected = [("first", "url1"), ("second", "url2")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_empty_alt_text(self):
        text = "![ ](url)"
        expected = [(" ", "url")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_empty_url(self):
        text = "![alt]()"
        expected = [("alt", "")]
        self.assertEqual(extract_markdown_images(text), expected)

    #def test_image_with_nested_brackets(self):
    #    text = "![nested [brackets]](url)"
    #    expected = [("nested [brackets]", "url")]
    #    self.assertEqual(extract_markdown_images(text), expected)

    def test_no_image(self):
        text = "No images here"
        self.assertEqual(extract_markdown_images(text), [])

    # ====================
    # Link extraction tests
    # ====================

    def test_single_link(self):
        text = "Go to [boot.dev](https://www.boot.dev)"
        expected = [("boot.dev", "https://www.boot.dev")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "[Link1](url1) and [Link2](url2)"
        expected = [("Link1", "url1"), ("Link2", "url2")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_empty_text(self):
        text = "[](url)"
        expected = [("", "url")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_empty_url(self):
        text = "[text]()"
        expected = [("text", "")]
        self.assertEqual(extract_markdown_links(text), expected)

    #def test_link_with_nested_brackets(self):
    #    text = "[nested [brackets]](url)"
    #    expected = [("nested [brackets]", "url")]
    #    self.assertEqual(extract_markdown_links(text), expected)

    def test_no_link(self):
        text = "No links here"
        self.assertEqual(extract_markdown_links(text), [])

    # ====================
    # Mixed content tests
    # ====================

    def test_links_and_images_together(self):
        text = "Here is ![img](img_url) and [link](link_url)"
        expected_images = [("img", "img_url")]
        expected_links = [("link", "link_url")]
        self.assertEqual(extract_markdown_images(text), expected_images)
        self.assertEqual(extract_markdown_links(text), expected_links)

    def test_image_and_link_same_brackets(self):
        text = "![image](url1) [link](url2)"
        expected_images = [("image", "url1")]
        expected_links = [("link", "url2")]
        self.assertEqual(extract_markdown_images(text), expected_images)
        self.assertEqual(extract_markdown_links(text), expected_links)

    def test_link_preceded_by_exclamation_not_matched(self):
        text = "![not a link](url)"
        self.assertEqual(extract_markdown_links(text), [])

if __name__ == "__main__":
    unittest.main()


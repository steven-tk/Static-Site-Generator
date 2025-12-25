import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            tag="a",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_single_prop(self):
        node = HTMLNode(
            tag="img",
            props={
                "src": "image.png",
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' src="image.png"'
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()

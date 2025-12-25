import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_different_text(self):
        node1 = TextNode("hello", TextType.PLAIN)
        node2 = TextNode("world", TextType.PLAIN)
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_type(self):
        node1 = TextNode("hello", TextType.PLAIN)
        node2 = TextNode("hello", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_equal_url_none_vs_value(self):
        node1 = TextNode("link", TextType.LINK, None)
        node2 = TextNode("link", TextType.LINK, "https://example.com")
        self.assertNotEqual(node1, node2)
    


if __name__ == "__main__":
    unittest.main()
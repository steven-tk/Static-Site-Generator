import unittest

from nodesplit import split_nodes_delimiter
from textnode import TextType, TextNode


class TestNodeSplit(unittest.TestCase):
    
        # ===============
        # NodeSplit Tests
        # ===============

    # Basic case
    def test_split_code(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ])

    # Multiple delimiters
    def test_split_multiple_bold(self):
        node = TextNode("This **is** very **bold**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(nodes, [
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.BOLD),
            TextNode(" very ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])

    # Invalid markdown
    def test_unmatched_delimiter_raises(self):
        node = TextNode("This **is broken", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    # Invalid markdown
    def test_non_text_nodes_untouched(self):
        node = TextNode("bold", TextType.BOLD)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(nodes, [node])

    #Multiple TEXT nodes
    def test_multiple_nodes_in_list(self):
        nodes = [
            TextNode("This is `code`", TextType.TEXT),
            TextNode(" and more text", TextType.TEXT),
        ]

        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and more text", TextType.TEXT),
        ])

    # Delimiter at start or end
    def test_delimiter_at_start(self):
        node = TextNode("**bold** text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(nodes, [
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_delimiter_at_end(self):
        node = TextNode("text **bold**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(nodes, [
            TextNode("text ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])

    # No delimiter present
    def test_no_delimiter_returns_original(self):
        node = TextNode("Just plain text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(nodes, [node])

    # Adjacent delimiters
    def test_empty_delimited_content(self):
        node = TextNode("This is `` code", TextType.TEXT)

        nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("", TextType.CODE, None),
            TextNode(" code", TextType.TEXT),
        ])



if __name__ == "__main__":
    unittest.main()
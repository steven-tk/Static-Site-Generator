import unittest
from nodesplit import text_to_textnodes
from textnode import TextNode, TextType


# ===============
# run with:
# python3 -m unittest discover -s src
# ===============


class TestTextToNodes(unittest.TestCase):

    # ===============
    # TextToNodes Tests
    # ===============

    def test_example_test(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(text)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ]
        )

    def test_plain_text_only(self):
        text = "Just plain text with no markdown"
        nodes = text_to_textnodes(text)

        self.assertEqual(
            nodes,
            [TextNode("Just plain text with no markdown", TextType.TEXT)],
        )

    def test_adjacent_markdown(self):
        text = "**bold**_italic_`code`"
        nodes = text_to_textnodes(text)

        self.assertEqual(
            nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_markdown_at_start_and_end(self):
        text = "**bold** text _italic_"
        nodes = text_to_textnodes(text)

        self.assertEqual(
            nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" text ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
        )

    def test_multiple_links(self):
        text = "[one](a)[two](b)[three](c)"
        nodes = text_to_textnodes(text)

        self.assertEqual(
            nodes,
            [
                TextNode("one", TextType.LINK, "a"),
                TextNode("two", TextType.LINK, "b"),
                TextNode("three", TextType.LINK, "c"),
            ],
        )


    def test_link_and_image_adjacent(self):
        text = "![img](img.png)[link](url)"
        nodes = text_to_textnodes(text)

        self.assertEqual(
            nodes,
            [
                TextNode("img", TextType.IMAGE, "img.png"),
                TextNode("link", TextType.LINK, "url"),
            ],
        )

    def test_no_empty_text_nodes(self):
        text = "**bold**"
        nodes = text_to_textnodes(text)

        for node in nodes:
            self.assertFalse(
                node.text_type == TextType.TEXT and node.text == ""
            )


if __name__ == "__main__":
    unittest.main()


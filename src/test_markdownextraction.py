import unittest
from nodesplit import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


# ===============
# run with:
# python3 -m unittest discover -s src
# ===============


class TestMarkdownExtraction(unittest.TestCase):

    # ===============
    # Markdown Extraction Tests
    # ===============

    # IMAGES
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_split_images_at_start(self):
        node = TextNode(
            "![alt](url) rest of text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("alt", TextType.IMAGE, "url"),
                TextNode(" rest of text", TextType.TEXT),
            ],
        )

    def test_split_images_at_end(self):
        node = TextNode(
            "Text before ![alt](url)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "url"),
            ],
        )

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("Start ![one](url1)", TextType.TEXT),
            TextNode(" middle ", TextType.TEXT),
            TextNode("![two](url2) end", TextType.TEXT),
        ]

        new_nodes = split_nodes_image(nodes)

        self.assertEqual(
            new_nodes,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "url2"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_split_images_non_text_nodes_untouched(self):
        node = TextNode("alt", TextType.IMAGE, "url")
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])


    # LINKS
    def test_split_links_basic(self):
        node = TextNode(
            "This is a [link](https://example.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "Links: [one](a) and [two](b)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("Links: ", TextType.TEXT),
                TextNode("one", TextType.LINK, "a"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.LINK, "b"),
            ],
        )

    def test_split_links_no_links(self):
        node = TextNode("No links here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_split_links_ignores_images(self):
        node = TextNode(
            "Text ![img](url) and [link](href)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text ![img](url) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "href"),
            ],
        )


if __name__ == "__main__":
    unittest.main()

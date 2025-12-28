import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, text_node_to_html_node

# Quickfix cause i can't be bothered right now
def assert_has_props(node: HTMLNode) -> dict[str, str]:
    assert node.props is not None
    return node.props


class TestTextToNode(unittest.TestCase):

        # ===============
        # TextNode to HTML Tests
        # ===============

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")

    def test_link(self):
        node = TextNode("Example", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Example")
        props = assert_has_props(html_node)
        self.assertEqual(props["href"], "https://example.com")
        self.assertEqual(props["target"], "_blank")

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        props = assert_has_props(html_node)
        self.assertEqual(props["src"], "image.png") # type: ignore[index]
        self.assertEqual(props["alt"], "Alt text") # type: ignore[index]

    def test_invalid_type_raises(self):
        node = TextNode("oops", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_link_to_html(self):
        node = TextNode("Example", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://example.com" target="_blank">Example</a>'
        )

    def test_image_to_html(self):
        node = TextNode("Alt text", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<img src="image.png" alt="Alt text"></img>'
        )

    def test_link_missing_url(self):
        node = TextNode("Example", TextType.LINK, None)
        html_node = text_node_to_html_node(node)
        props = assert_has_props(html_node)
        self.assertEqual(props["href"], None)

    def test_image_empty_alt(self):
        node = TextNode("", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        props = assert_has_props(html_node)
        self.assertEqual(props["alt"], "")

    def test_invalid_text_type_object(self):
        class FakeType:
            pass

        node = TextNode("oops", FakeType())
        with self.assertRaises(Exception):
            text_node_to_html_node(node)



if __name__ == "__main__":
    unittest.main()

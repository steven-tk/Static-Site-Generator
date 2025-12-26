import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    # ===============
    # HTMLNode Tests
    # ===============

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


class TestLeafNode(unittest.TestCase):

    # ===============
    # LeafNode Tests
    # ===============

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_short_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_img_tag(self):
        node = LeafNode("img", "Image here", props={"src": "image.png", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="An image">Image here</img>')

    def test_leaf_to_html_missing_value_raises(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()
    

class TestParentNode(unittest.TestCase):

    # ===============
    # ParentNode Tests
    # ===============

    # provided examples
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
             "<div><span><b>grandchild</b></span></div>",
         )

    # Parent with multiple LeafNode children (mix of tags and raw text)
    def test_parent_multiple_leaf_children(self):
        child1 = LeafNode("b", "Bold")
        child2 = LeafNode(None, " plain text ")
        child3 = LeafNode("i", "Italic")
        parent = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent.to_html(),
            "<div><b>Bold</b> plain text <i>Italic</i></div>"
        )

    # Nested ParentNodes (grandchildren)
    def test_parent_nested(self):
        grandchild = LeafNode("span", "inner")
        child = ParentNode("p", [grandchild])
        parent = ParentNode("section", [child])
        self.assertEqual(
            parent.to_html(),
            "<section><p><span>inner</span></p></section>"
        )

    # Parent with props/attributes
    def test_parent_with_props(self):
        child = LeafNode("a", "Click me", {"href": "https://example.com"})
        parent = ParentNode("div", [child], props={"id": "main", "class": "container"})
        self.assertEqual(
            parent.to_html(),
            '<div id="main" class="container"><a href="https://example.com">Click me</a></div>'
        )

    # Empty children list should raise ValueError
    def test_parent_empty_children_raises(self):
        with self.assertRaises(ValueError):
            parent = ParentNode("div", [])
            parent.to_html()

    # Missing tag should raise ValueError
    def test_parent_missing_tag_raises(self):
        child = LeafNode("p", "Text")
        with self.assertRaises(ValueError):
            parent = ParentNode(None, [child])
            parent.to_html()

    # Multiple nested levels (stress test)
    def test_parent_multiple_nested_levels(self):
        leaf1 = LeafNode("i", "Italic")
        leaf2 = LeafNode(None, " normal ")
        nested = ParentNode("span", [leaf1, leaf2])
        parent = ParentNode("div", [nested, LeafNode("b", "Bold")])
        self.assertEqual(
            parent.to_html(),
            "<div><span><i>Italic</i> normal </span><b>Bold</b></div>"
        )

if __name__ == "__main__":
    unittest.main()


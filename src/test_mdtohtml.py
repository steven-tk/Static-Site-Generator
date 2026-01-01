import unittest
from markdown import markdown_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode


# ===============
# run with:
# python3 -m unittest discover -s src
# ===============


class TestMarkdownToHTML(unittest.TestCase):

    # ===============
    # MD to HTML Tests
    # ===============

    # example mixed paragraph
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    # example codeblock
    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    # Headings
    def test_headings(self):
        md = """
    # Heading 1

    ## Heading 2

    ### Heading 3
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading 1</h1>"
            "<h2>Heading 2</h2>"
            "<h3>Heading 3</h3>"
            "</div>"
        )

    # unordered list
    def test_unordered_list(self):
        md = """
    - first item
    - second item
    - third item
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<ul>"
            "<li>first item</li>"
            "<li>second item</li>"
            "<li>third item</li>"
            "</ul>"
            "</div>"
        )

    # ordered list
    def test_ordered_list(self):
        md = """
    1. first
    2. second
    3. third
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<ol>"
            "<li>first</li>"
            "<li>second</li>"
            "<li>third</li>"
            "</ol>"
            "</div>"
        )

    # quote block
    def test_blockquote(self):
        md = """
    > this is a quote
    > spanning multiple lines
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<blockquote>"
            "this is a quote spanning multiple lines"
            "</blockquote>"
            "</div>"
        )

    # mixed doc
    def test_mixed_blocks(self):
        md = """
    # Title

    This is a paragraph with **bold** text.

    - one
    - two

    > quoted text
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<h1>Title</h1>"
            "<p>This is a paragraph with <b>bold</b> text.</p>"
            "<ul><li>one</li><li>two</li></ul>"
            "<blockquote>quoted text</blockquote>"
            "</div>"
        )

    # whitespace normalization
    def test_paragraph_line_joining(self):
        md = """
    This paragraph
    has multiple
    lines
    """

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>This paragraph has multiple lines</p></div>"
        )

    """  # empty
    def test_empty_markdown(self):
        md = ""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(html, "<div></div>") """



if __name__ == "__main__":
    unittest.main()


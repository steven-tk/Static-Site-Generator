import unittest
from markdown import markdown_to_blocks


# ===============
# run with:
# python3 -m unittest discover -s src
# ===============


class TestPLACEHOLDER(unittest.TestCase):

    # ===============
    # PLACEHOLDER Tests
    # ===============

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_trims_outer_whitespace(self):
        md = """

        This is a paragraph

        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph"])

    def test_multiple_blank_lines(self):
        md = """
    Paragraph one


    Paragraph two



    Paragraph three
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph one",
                "Paragraph two",
                "Paragraph three",
            ],
        )

    def test_single_block_no_blank_lines(self):
        md = "This is one paragraph\nstill same paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is one paragraph\nstill same paragraph"]
        )

    def test_list_is_single_block(self):
        md = """
    - item one
    - item two
    - item three
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["- item one\n- item two\n- item three"]
        )

    def test_blocks_trim_indentation(self):
        md = """
            Paragraph one

                Paragraph two
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph one",
                "Paragraph two",
            ],
        )

    def test_empty_input(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])


    def test_whitespace_only_input(self):
        md = "   \n\n   \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

if __name__ == "__main__":
    unittest.main()

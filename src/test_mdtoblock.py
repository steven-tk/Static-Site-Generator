import unittest
from markdown import markdown_to_blocks
from blocknode import BlockType, block_to_block_type


# ===============
# run with:
# python3 -m unittest discover -s src
# ===============


class TestBlockSplit(unittest.TestCase):

    # ===============
    # BlockSplit Tests
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


class TestBlockType(unittest.TestCase):

    # ===============
    # BlockType Tests
    # ===============

    def test_heading_levels(self):
        for i in range(1, 7):
            block = "#" * i + " heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEAD)

    def test_code_block(self):
        block = "```\ncode here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> quote\n> still quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- item one\n- item two"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)

    def test_invalid_ordered_list(self):
        block = "1. first\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)

    def test_mixed_block_is_paragraph(self):
        block = "> quote\nnot quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)






if __name__ == "__main__":
    unittest.main()

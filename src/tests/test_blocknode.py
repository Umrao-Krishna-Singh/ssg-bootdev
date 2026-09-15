import unittest

from blocks_parsing.blocknode import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):

    # -------------------------
    # Headings
    # -------------------------

    def test_heading(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING,
        )

    def test_heading_with_1_to_6_hashes(self):
        for hashes in range(1, 7):
            block = f"{'#' * hashes} Heading"

            self.assertEqual(
                block_to_block_type(block),
                BlockType.HEADING,
            )

    def test_heading_with_7_hashes_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("####### Heading"),
            BlockType.PARA,
        )

    def test_heading_requires_space(self):
        self.assertEqual(
            block_to_block_type("#Heading"),
            BlockType.PARA,
        )

    # -------------------------
    # Code blocks
    # -------------------------

    def test_code_block(self):
        block = "```\nprint('hello')\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_multiline_code_block(self):
        block = "```\nline 1\nline 2\nline 3\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_code_block_must_start_with_backticks_and_newline(self):
        block = "```print('hello')\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARA,
        )

    def test_code_block_must_end_with_backticks(self):
        block = "```\nprint('hello')"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARA,
        )

    # -------------------------
    # Quote blocks
    # -------------------------

    def test_quote_block(self):
        block = "> Hello world"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_multiline_quote_block(self):
        block = "> Line one\n> Line two\n> Line three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_quote_does_not_require_space_after_greater_than(self):
        block = ">Line one\n>Line two"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_quote_with_optional_spaces(self):
        block = "> Line one\n>Line two\n> Line three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_quote_requires_every_line_to_start_with_greater_than(self):
        block = "> Line one\nLine two\n> Line three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARA,
        )

    # -------------------------
    # Unordered lists
    # -------------------------

    def test_unordered_list(self):
        block = "- Item one"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UL,
        )

    def test_multiline_unordered_list(self):
        block = "- Item one\n- Item two\n- Item three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UL,
        )

    def test_unordered_list_requires_space(self):
        block = "-Item one\n-Item two"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARA,
        )

    def test_unordered_list_requires_every_line_to_start_with_dash(self):
        block = "- Item one\nItem two\n- Item three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARA,
        )

    # -------------------------
    # Ordered lists
    # -------------------------

    def test_ordered_list(self):
        block = "1. Item one"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.OL,
        )

    def test_multiline_ordered_list(self):
        block = "1. Item one\n2. Item two\n3. Item three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.OL,
        )

    def test_ordered_list_must_start_at_one(self):
        block = "2. Item one\n3. Item two"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARA,
        )

    def test_ordered_list_numbers_must_increment(self):
        block = "1. Item one\n3. Item three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARA,
        )

    def test_ordered_list_rejects_decreasing_numbers(self):
        block = "1. Item one\n2. Item two\n1. Item one again"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARA,
        )

    def test_ordered_list_requires_space_after_dot(self):
        block = "1.Item one\n2.Item two"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARA,
        )

    def test_ordered_list_requires_every_line_to_be_ordered(self):
        block = "1. Item one\n2. Item two\nSomething else"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARA,
        )

    # -------------------------
    # Paragraphs
    # -------------------------

    def test_normal_paragraph(self):
        block = "This is a normal paragraph."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARA,
        )

    def test_multiline_paragraph(self):
        block = "This is line one.\nThis is line two."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARA,
        )


if __name__ == "__main__":
    unittest.main()

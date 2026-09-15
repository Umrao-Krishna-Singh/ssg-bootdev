from unittest import TestCase

from mkdwn_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(TestCase):
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

    def test_single_block(self):
        md = "This is a single paragraph."

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "This is a single paragraph.",
            ],
        )

    def test_empty_markdown(self):
        self.assertEqual(
            markdown_to_blocks(""),
            [],
        )

    def test_only_whitespace(self):
        self.assertEqual(
            markdown_to_blocks("   \n\n   \n\n   "),
            [],
        )

    def test_leading_and_trailing_whitespace(self):
        md = """
        
        This is a paragraph.
        
        """

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "This is a paragraph.",
            ],
        )

    def test_leading_and_trailing_newlines(self):
        md = "\n\n\nThis is a paragraph.\n\n\n"

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "This is a paragraph.",
            ],
        )

    def test_multiple_blank_lines(self):
        md = """
First block.


Second block.



Third block.
"""

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "First block.",
                "Second block.",
                "Third block.",
            ],
        )

    def test_multiline_block(self):
        md = """First line of paragraph
Second line of paragraph
Third line of paragraph

Another block
"""

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "First line of paragraph\nSecond line of paragraph\nThird line of paragraph",
                "Another block",
            ],
        )

    def test_heading_and_paragraph(self):
        md = """# Heading

This is a paragraph.
"""

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# Heading",
                "This is a paragraph.",
            ],
        )

    def test_multiple_markdown_block_types(self):
        md = """# Heading

This is **bold** and _italic_.

- First item
- Second item
- Third item
"""

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# Heading",
                "This is **bold** and _italic_.",
                "- First item\n- Second item\n- Third item",
            ],
        )

    def test_blank_lines_do_not_create_empty_blocks(self):
        md = """First block

 
 
Second block

   
Third block
"""

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "First block",
                "Second block",
                "Third block",
            ],
        )

    def test_whitespace_around_blocks(self):
        md = """   First block   

   Second block   
"""

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "First block",
                "Second block",
            ],
        )

    def test_inline_markdown_is_preserved(self):
        md = """This has **bold** and _italic_.

This has `code` and a [link](https://example.com).
"""

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "This has **bold** and _italic_.",
                "This has `code` and a [link](https://example.com).",
            ],
        )

    def test_image_markdown_is_preserved(self):
        md = """Here is an ![image](https://example.com/image.png).

This is another block.
"""

        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Here is an ![image](https://example.com/image.png).",
                "This is another block.",
            ],
        )

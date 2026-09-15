import unittest

from generator import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        markdown = "# Hello"

        self.assertEqual(
            extract_title(markdown),
            "Hello",
        )

    def test_extract_title_strips_whitespace(self):
        markdown = "#    Hello World   "

        self.assertEqual(
            extract_title(markdown),
            "Hello World",
        )

    def test_extract_title_from_multiple_lines(self):
        markdown = """
# Hello World

This is a paragraph.

## Subtitle

More text.
"""

        self.assertEqual(
            extract_title(markdown),
            "Hello World",
        )

    def test_extract_title_ignores_h2(self):
        markdown = """
## Not the title

Some text.
"""

        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_ignores_multiple_hashes(self):
        markdown = """
### Not the title
## Also not the title
"""

        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_raises_when_no_h1(self):
        markdown = """
This is a paragraph.

## Heading 2

### Heading 3
"""

        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()

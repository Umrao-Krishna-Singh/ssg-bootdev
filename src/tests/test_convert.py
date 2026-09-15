import unittest

from convert import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):

    # -------------------------
    # Paragraphs
    # -------------------------

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

    # -------------------------
    # Headings
    # -------------------------

    def test_heading(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading 1</h1>"
            "<h2>Heading 2</h2>"
            "<h3>Heading 3</h3>"
            "<h4>Heading 4</h4>"
            "<h5>Heading 5</h5>"
            "<h6>Heading 6</h6>"
            "</div>",
        )

    def test_heading_with_inline_markdown(self):
        md = "# This is **bold** and _italic_"

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h1>This is <b>bold</b> and <i>italic</i></h1></div>",
        )

    # -------------------------
    # Code blocks
    # -------------------------

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

    def test_codeblock_preserves_inline_markdown(self):
        md = """
```

**bold**
*italic*
`code`
[link](https://example.com)
![image](image.png)

```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>**bold**\n"
            "*italic*\n"
            "`code`\n"
            "[link](https://example.com)\n"
            "![image](image.png)\n"
            "</code></pre></div>",
        )

    # -------------------------
    # Unordered lists
    # -------------------------

    def test_unordered_list(self):
        md = """
- Item one
- Item two
- Item three
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<ul>"
            "<li>Item one</li>"
            "<li>Item two</li>"
            "<li>Item three</li>"
            "</ul>"
            "</div>",
        )

    def test_unordered_list_with_inline_markdown(self):
        md = """
- **Bold item**
- _Italic item_
- Item with `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<ul>"
            "<li><b>Bold item</b></li>"
            "<li><i>Italic item</i></li>"
            "<li>Item with <code>code</code></li>"
            "</ul>"
            "</div>",
        )

    # -------------------------
    # Ordered lists
    # -------------------------

    def test_ordered_list(self):
        md = """
1. Item one
2. Item two
3. Item three
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<ol>"
            "<li>Item one</li>"
            "<li>Item two</li>"
            "<li>Item three</li>"
            "</ol>"
            "</div>",
        )

    def test_ordered_list_with_inline_markdown(self):
        md = """
1. **First item**
2. _Second item_
3. Item with `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<ol>"
            "<li><b>First item</b></li>"
            "<li><i>Second item</i></li>"
            "<li>Item with <code>code</code></li>"
            "</ol>"
            "</div>",
        )

    # -------------------------
    # Block quotes
    # -------------------------

    def test_blockquote(self):
        md = """
> This is a quote
> with multiple lines
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<blockquote>This is a quote with multiple lines</blockquote>"
            "</div>",
        )

    def test_blockquote_with_inline_markdown(self):
        md = """
> This is **bold** and _italic_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<blockquote>This is <b>bold</b> and <i>italic</i></blockquote>"
            "</div>",
        )

    # -------------------------
    # Links
    # -------------------------

    def test_paragraph_with_link(self):
        md = """
This is a [link](https://example.com)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            '<div><p>This is a <a href="https://example.com">link</a></p></div>',
        )

    # -------------------------
    # Images
    # -------------------------

    def test_paragraph_with_image(self):
        md = """
Here is an ![image](https://example.com/image.png)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            '<div><p>Here is an <img src="https://example.com/image.png" alt="image"></img></p></div>',
        )

    # -------------------------
    # Mixed document
    # -------------------------

    def test_mixed_document(self):
        md = """
# My Document

This is a **paragraph** with _italic_ text.

- First item
- Second item
- Third item

## Code

```

const x = **not bold**;
const y = *not italic*;

```

> This is a quote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<h1>My Document</h1>"
            "<p>This is a <b>paragraph</b> with <i>italic</i> text.</p>"
            "<ul>"
            "<li>First item</li>"
            "<li>Second item</li>"
            "<li>Third item</li>"
            "</ul>"
            "<h2>Code</h2>"
            "<pre><code>const x = **not bold**;\n"
            "const y = *not italic*;\n"
            "</code></pre>"
            "<blockquote>This is a quote</blockquote>"
            "</div>",
        )

    # -------------------------
    # Document structure
    # -------------------------

    def test_returns_single_div_parent(self):
        md = """
# Heading

Paragraph
"""

        node = markdown_to_html_node(md)

        self.assertEqual(node.tag, "div")
        self.assertIsNotNone(node.children)

        children = node.children
        assert children is not None

        self.assertEqual(len(children), 2)

    def test_block_order_is_preserved(self):
        md = """
# Heading

First paragraph

- Item one
- Item two

Second paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading</h1>"
            "<p>First paragraph</p>"
            "<ul><li>Item one</li><li>Item two</li></ul>"
            "<p>Second paragraph</p>"
            "</div>",
        )

from unittest import TestCase

from textnode import TextNode, TextType
from mkdwn_to_textnode import (
    split_nodes_delimiter,
    extract_markdown_images,
    split_nodes_images_delimiter,
    split_nodes_link_delimiter,
)


class TestSplitNodesDelimiter(TestCase):

    def test_single_delimited_node(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold_text(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ],
        )

    def test_italic_text(self):
        node = TextNode(
            "This is an _italic phrase_ in the middle",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "_",
            TextType.ITALIC,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("italic phrase", TextType.ITALIC),
                TextNode(" in the middle", TextType.TEXT),
            ],
        )

    def test_multiple_delimited_sections(self):
        node = TextNode(
            "This is **bold** and this is **also bold**",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and this is ", TextType.TEXT),
                TextNode("also bold", TextType.BOLD),
            ],
        )

    def test_delimiter_at_start(self):
        node = TextNode(
            "**bold** text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_delimiter_at_end(self):
        node = TextNode(
            "text **bold**",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("text ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_entire_text_is_delimited(self):
        node = TextNode(
            "**entire text is bold**",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("entire text is bold", TextType.BOLD),
            ],
        )

    def test_text_without_delimiter(self):
        node = TextNode(
            "This is just normal text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is just normal text", TextType.TEXT),
            ],
        )

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("This is normal text", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(
            nodes,
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
                TextNode("This is normal text", TextType.TEXT),
            ],
        )

    def test_non_text_nodes_are_unchanged(self):
        node1 = TextNode(
            "This is **bold** text",
            TextType.TEXT,
        )

        node2 = TextNode(
            "Already bold",
            TextType.BOLD,
        )

        new_nodes = split_nodes_delimiter(
            [node1, node2],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
                TextNode("Already bold", TextType.BOLD),
            ],
        )

    def test_code_delimiter(self):
        node = TextNode(
            "Run `npm install` in your terminal",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("Run ", TextType.TEXT),
                TextNode("npm install", TextType.CODE),
                TextNode(" in your terminal", TextType.TEXT),
            ],
        )

    def test_multiple_code_sections(self):
        node = TextNode(
            "Use `npm install` and then run `npm start`",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("npm install", TextType.CODE),
                TextNode(" and then run ", TextType.TEXT),
                TextNode("npm start", TextType.CODE),
            ],
        )

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)

        new_nodes = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
            ],
        )

    def test_empty_delimited_text(self):
        node = TextNode(
            "This is **** text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_unmatched_delimiter_raises_error(self):
        node = TextNode(
            "This is **bold text",
            TextType.TEXT,
        )

        with self.assertRaises(Exception):
            split_nodes_delimiter(
                [node],
                "**",
                TextType.BOLD,
            )

    # images
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_multiple_markdown_images(self):
        text = (
            "This is text with ![image 1](https://example.com/1.png) "
            "and ![image 2](https://example.com/2.jpg)"
        )

        matches = extract_markdown_images(text)

        self.assertListEqual(
            [
                ("image 1", "https://example.com/1.png"),
                ("image 2", "https://example.com/2.jpg"),
            ],
            matches,
        )

    def test_extract_markdown_image_at_start(self):
        text = "![image](https://example.com/image.png) some text"

        matches = extract_markdown_images(text)

        self.assertListEqual(
            [("image", "https://example.com/image.png")],
            matches,
        )

    def test_extract_markdown_image_at_end(self):
        text = "Some text ![image](https://example.com/image.png)"

        matches = extract_markdown_images(text)

        self.assertListEqual(
            [("image", "https://example.com/image.png")],
            matches,
        )

    def test_extract_markdown_image_only(self):
        text = "![image](https://example.com/image.png)"

        matches = extract_markdown_images(text)

        self.assertListEqual(
            [("image", "https://example.com/image.png")],
            matches,
        )

    def test_extract_markdown_images_with_no_images(self):
        text = "This is just some normal text."

        matches = extract_markdown_images(text)

        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_empty_text(self):
        matches = extract_markdown_images("")

        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_multiple_lines(self):
        text = """
        First ![image 1](https://example.com/1.png)
        Second ![image 2](https://example.com/2.png)
        """

        matches = extract_markdown_images(text)

        self.assertListEqual(
            [
                ("image 1", "https://example.com/1.png"),
                ("image 2", "https://example.com/2.png"),
            ],
            matches,
        )

    def test_extract_markdown_image_with_spaces_in_alt_text(self):
        text = "![this is an image](https://example.com/image.png)"

        matches = extract_markdown_images(text)

        self.assertListEqual(
            [("this is an image", "https://example.com/image.png")],
            matches,
        )

    def test_extract_markdown_image_does_not_match_link(self):
        text = "[image](https://example.com/image.png)"

        matches = extract_markdown_images(text)

        self.assertListEqual([], matches)


class TestSplitNodesImage(TestCase):

    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_delimiter([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
            ],
            new_nodes,
        )

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/1.png) "
            "and another ![second image](https://example.com/2.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_delimiter([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/1.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://example.com/2.png",
                ),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://example.com/image.png) is here",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_delimiter([node])

        self.assertListEqual(
            [
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
                TextNode(" is here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode(
            "This is an ![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_delimiter([node])

        self.assertListEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
            ],
            new_nodes,
        )

    def test_split_image_only(self):
        node = TextNode(
            "![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_delimiter([node])

        self.assertListEqual(
            [
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
            ],
            new_nodes,
        )

    def test_text_without_image_is_unchanged(self):
        node = TextNode(
            "This is just normal text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_delimiter([node])

        self.assertListEqual(
            [
                TextNode(
                    "This is just normal text",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)

        new_nodes = split_nodes_images_delimiter([node])

        self.assertListEqual(
            [TextNode("", TextType.TEXT)],
            new_nodes,
        )

    def test_image_with_spaces_in_alt_text(self):
        node = TextNode(
            "See ![this is an image](https://example.com/image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_delimiter([node])

        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode(
                    "this is an image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
            ],
            new_nodes,
        )

    def test_image_does_not_extract_normal_link(self):
        node = TextNode(
            "This is a [link](https://example.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_delimiter([node])

        self.assertListEqual(
            [
                TextNode(
                    "This is a [link](https://example.com)",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_existing_non_text_node_is_unchanged(self):
        image_node = TextNode(
            "already an image",
            TextType.IMAGE,
            "https://example.com/image.png",
        )

        new_nodes = split_nodes_images_delimiter([image_node])

        self.assertListEqual(
            [image_node],
            new_nodes,
        )

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode(
                "First ![image](https://example.com/1.png)",
                TextType.TEXT,
            ),
            TextNode(
                "Second ![image](https://example.com/2.png)",
                TextType.TEXT,
            ),
        ]

        new_nodes = split_nodes_images_delimiter(nodes)

        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/1.png",
                ),
                TextNode("Second ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/2.png",
                ),
            ],
            new_nodes,
        )

    def test_multiple_images_without_text_between(self):
        node = TextNode(
            "![first](https://example.com/1.png)![second](https://example.com/2.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_delimiter([node])

        self.assertListEqual(
            [
                TextNode(
                    "first",
                    TextType.IMAGE,
                    "https://example.com/1.png",
                ),
                TextNode(
                    "second",
                    TextType.IMAGE,
                    "https://example.com/2.png",
                ),
            ],
            new_nodes,
        )

    def test_image_with_url_containing_query_parameters(self):
        node = TextNode(
            "Image: ![photo](https://example.com/image.png?width=100&height=200)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images_delimiter([node])

        self.assertListEqual(
            [
                TextNode("Image: ", TextType.TEXT),
                TextNode(
                    "photo",
                    TextType.IMAGE,
                    "https://example.com/image.png?width=100&height=200",
                ),
            ],
            new_nodes,
        )


class TestSplitNodesLink(TestCase):

    def test_split_single_link(self):
        node = TextNode(
            "This is text with a [link](https://example.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link_delimiter([node])

        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://example.com",
                ),
            ],
            new_nodes,
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with a [Google](https://google.com) "
            "and [GitHub](https://github.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link_delimiter([node])

        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "GitHub",
                    TextType.LINK,
                    "https://github.com",
                ),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode(
            "[Google](https://google.com) is a search engine",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link_delimiter([node])

        self.assertListEqual(
            [
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
                TextNode(" is a search engine", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode(
            "Visit [Google](https://google.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link_delimiter([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
            ],
            new_nodes,
        )

    def test_split_link_only(self):
        node = TextNode(
            "[Google](https://google.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link_delimiter([node])

        self.assertListEqual(
            [
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
            ],
            new_nodes,
        )

    def test_text_without_link_is_unchanged(self):
        node = TextNode(
            "This is just normal text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link_delimiter([node])

        self.assertListEqual(
            [
                TextNode(
                    "This is just normal text",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)

        new_nodes = split_nodes_link_delimiter([node])

        self.assertListEqual(
            [TextNode("", TextType.TEXT)],
            new_nodes,
        )

    def test_link_with_spaces_in_anchor_text(self):
        node = TextNode(
            "Visit [the Google website](https://google.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link_delimiter([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "the Google website",
                    TextType.LINK,
                    "https://google.com",
                ),
            ],
            new_nodes,
        )

    def test_link_does_not_extract_image(self):
        node = TextNode(
            "This is an ![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link_delimiter([node])

        self.assertListEqual(
            [
                TextNode(
                    "This is an ![image](https://example.com/image.png)",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_existing_non_text_node_is_unchanged(self):
        link_node = TextNode(
            "already a link",
            TextType.LINK,
            "https://example.com",
        )

        new_nodes = split_nodes_link_delimiter([link_node])

        self.assertListEqual(
            [link_node],
            new_nodes,
        )

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode(
                "Visit [Google](https://google.com)",
                TextType.TEXT,
            ),
            TextNode(
                "Visit [GitHub](https://github.com)",
                TextType.TEXT,
            ),
        ]

        new_nodes = split_nodes_link_delimiter(nodes)

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "GitHub",
                    TextType.LINK,
                    "https://github.com",
                ),
            ],
            new_nodes,
        )

    def test_multiple_links_without_text_between(self):
        node = TextNode(
            "[Google](https://google.com)[GitHub](https://github.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link_delimiter([node])

        self.assertListEqual(
            [
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
                TextNode(
                    "GitHub",
                    TextType.LINK,
                    "https://github.com",
                ),
            ],
            new_nodes,
        )

    def test_link_with_url_containing_query_parameters(self):
        node = TextNode(
            "Visit [search](https://example.com/search?q=python&page=1)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link_delimiter([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "search",
                    TextType.LINK,
                    "https://example.com/search?q=python&page=1",
                ),
            ],
            new_nodes,
        )


class TestSplitNodesImageAndLink(TestCase):

    def test_mixed_image_and_link(self):
        node = TextNode(
            "Visit [Google](https://google.com) and "
            "see ![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        link_nodes = split_nodes_link_delimiter([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
                TextNode(
                    " and see ![image](https://example.com/image.png)",
                    TextType.TEXT,
                ),
            ],
            link_nodes,
        )

        image_nodes = split_nodes_images_delimiter(link_nodes)

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
                TextNode(" and see ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
            ],
            image_nodes,
        )

    def test_split_link_then_image(self):
        node = TextNode(
            "Visit [Google](https://google.com) and "
            "see ![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        nodes = split_nodes_link_delimiter([node])
        nodes = split_nodes_images_delimiter(nodes)

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
                TextNode(" and see ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
            ],
            nodes,
        )

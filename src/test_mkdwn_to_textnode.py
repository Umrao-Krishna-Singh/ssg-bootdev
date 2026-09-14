from unittest import TestCase

from textnode import TextNode, TextType
from mkdwn_to_textnode import split_nodes_delimiter


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

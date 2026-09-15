import unittest
from textnode_parsing.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_html_eq(self):
        node = HTMLNode(
            tag="a",
            value="My link",
            props={"href": "https://boot.dev"},
        )

        node_prop = ' href="https://boot.dev"'

        self.assertEqual(node.props_to_html(), node_prop)
        node2 = HTMLNode(
            tag="a",
            value="My link",
        )

        node2_prop = ""
        self.assertEqual(node2.props_to_html(), node2_prop)

        node3 = HTMLNode(
            tag="a",
            value="My link",
            props={"href": "https://boot.dev", "target": "_blank"},
        )

        node3_prop = ' href="https://boot.dev" target="_blank"'
        self.assertEqual(node3.props_to_html(), node3_prop)


if __name__ == "__main__":
    unittest.main()

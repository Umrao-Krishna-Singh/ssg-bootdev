import unittest
from htmlnode import HTMLNode


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

    # def test_neq(self):
    #     node = HTMLNode("This is a type test text node", )
    #     node2 = HTMLNode("This is a type test text node", )
    #     self.assertNotEqual(node, node2)

    # def test_url_eq(self):
    #     node = HTMLNode("This is a text node", )
    #     node2 = HTMLNode(
    #         "This is not a text node", , "https://www.boot.dev"
    #     )
    #     self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()

import unittest
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_grandchildren(self):
        grandchild_1 = LeafNode("b", "grandchild 1")
        grandchild_2 = LeafNode("i", "grandchild 2")
        grandchild_3 = LeafNode("b", "grandchild 3")
        grandchild_4 = LeafNode("i", "grandchild 4")

        child_1 = ParentNode("span", [grandchild_1, grandchild_2])
        child_2 = ParentNode("div", [grandchild_3, grandchild_4])

        parent_node = ParentNode("section", [child_1, child_2])

        self.assertEqual(
            parent_node.to_html(),
            "<section>"
            "<span><b>grandchild 1</b><i>grandchild 2</i></span>"
            "<div><b>grandchild 3</b><i>grandchild 4</i></div>"
            "</section>",
        )

    def test_to_html_with_multiple_grandchildren_and_props(self):
        grandchild_1 = LeafNode(
            "b",
            "grandchild 1",
            {"class": "bold", "id": "grandchild-1"},
        )
        grandchild_2 = LeafNode(
            "i",
            "grandchild 2",
        )
        grandchild_3 = LeafNode(
            "b",
            "grandchild 3",
            {"class": "highlight"},
        )
        grandchild_4 = LeafNode(
            "i",
            "grandchild 4",
            {"data-test": "grandchild-4"},
        )

        child_1 = ParentNode(
            "span",
            [grandchild_1, grandchild_2],
            {"class": "child-1"},
        )
        child_2 = ParentNode(
            "div",
            [grandchild_3, grandchild_4],
            {"id": "child-2"},
        )

        parent_node = ParentNode(
            "section",
            [child_1, child_2],
            {"class": "parent", "id": "parent"},
        )

        self.assertEqual(
            parent_node.to_html(),
            '<section class="parent" id="parent">'
            '<span class="child-1">'
            '<b class="bold" id="grandchild-1">grandchild 1</b>'
            "<i>grandchild 2</i>"
            "</span>"
            '<div id="child-2">'
            '<b class="highlight">grandchild 3</b>'
            '<i data-test="grandchild-4">grandchild 4</i>'
            "</div>"
            "</section>",
        )


if __name__ == "__main__":
    unittest.main()

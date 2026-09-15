from enum import Enum
from .leafnode import LeafNode
from .htmlnode import HTMLNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        else:
            return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def get_type(self) -> TextType:
        return self.text_type

    def get_text(self) -> str:
        return self.text

    def get_url(self) -> str | None:
        return self.url


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.get_type():
        case TextType.TEXT:
            return LeafNode(value=text_node.get_text())
        case TextType.BOLD:
            return LeafNode(value=text_node.get_text(), tag="b")
        case TextType.ITALIC:
            return LeafNode(value=text_node.get_text(), tag="i")
        case TextType.CODE:
            return LeafNode(value=text_node.get_text(), tag="code")
        case TextType.LINK:
            return LeafNode(
                value=text_node.get_text(), tag="a", props={"href": text_node.get_url()}
            )
        case TextType.IMAGE:
            return LeafNode(
                value="",
                tag="img",
                props={
                    "src": text_node.get_url(),
                    "alt": text_node.get_text(),
                },
            )
        case _:
            raise ValueError(
                f"Text modifier type must be one of {', '.join(item.value for item in TextType)}\nYou have entered {text_node.get_type()}"
            )

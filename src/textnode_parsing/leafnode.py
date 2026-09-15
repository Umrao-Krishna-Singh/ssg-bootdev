from typing import Dict, Optional
from .htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        props: Optional[Dict] = None,
    ) -> None:
        super().__init__()
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return f"{self.value}"
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}></{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self, _level=0) -> str:
        return f"==========LEAF NODE ELEMENT========== TAG:<{self.tag}> |||| VALUE:<{self.value}> |||| PROPS:<{self.props_to_html()}>"

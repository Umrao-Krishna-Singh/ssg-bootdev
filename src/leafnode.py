from typing import Dict, Optional
from htmlnode import HTMLNode


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
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"\n==========LEAF NODE ELEMENT==========\nTAG:{self.tag}\nVALUE:{self.value}\nPROPS:{self.props_to_html()}\n===================="

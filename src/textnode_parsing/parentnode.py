from typing import List, Dict, Optional
from .htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: List[HTMLNode],
        props: Optional[Dict] = None,
    ) -> None:
        super().__init__()
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Parent nodes must have tag")
        if not self.children:
            raise ValueError("Parent nodes must have children")

        html = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"

        return html

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        else:
            props = ""
            for key in self.props:
                props += f' {key}="{self.props[key]}"'

            return props

    def __repr__(self, level: int = 0) -> str:
        children = ""
        if self.children:
            for child in self.children:
                space = "   "
                children += f"\n{space*(1-level)}child@{level-1}>>" + child.__repr__(-1)

        return f"==========PARENT NODE ELEMENT========== TAG:<{self.tag}> |||| PROPS:<{self.props_to_html()}> |||| CHILDREN:{children}"

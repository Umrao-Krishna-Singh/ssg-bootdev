from typing import List, Dict, Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List["HTMLNode"]] = None,
        props: Optional[Dict] = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplemented(
            "This method needs to be implemented by inheriting classes"
        )

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

        return f"==========HTML NODE ELEMENT========== TAG:<{self.tag}> |||| VALUE:<{self.value}> |||| PROPS:{self.props_to_html()} |||| CHILDREN:{children}"

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

    def __repr__(self) -> str:
        children = ""

        if self.children:
            for child in self.children:
                children += f"{child}"

        return f"\n==========HTML NODE ELEMENT==========\nTAG:{self.tag}\nVALUE:{self.value}\nPROPS:{self.props_to_html()}\nCHILDREN:{children}\n===================="

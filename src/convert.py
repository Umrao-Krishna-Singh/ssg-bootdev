from enum import Enum
from textnode_parsing.htmlnode import HTMLNode
from blocks_parsing.mkdwn_to_blocks import markdown_to_blocks
from blocks_parsing.blocknode import block_to_block_type, BlockType
from textnode_parsing.textnode import TextType, TextNode, text_node_to_html_node
from textnode_parsing.mkdwn_to_textnode import text_to_textnodes
from textnode_parsing.parentnode import ParentNode
import re


class HtmlTagType(Enum):
    PARA = "p"
    QUOTE = "blockquote"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    UL = "ul"
    OL = "ol"
    CODE = "pre"


def mk_type_to_html_tag(block_type: BlockType) -> HtmlTagType:
    match block_type:
        case BlockType.PARA:
            return HtmlTagType.PARA
        case BlockType.H1:
            return HtmlTagType.H1
        case BlockType.H2:
            return HtmlTagType.H2
        case BlockType.H3:
            return HtmlTagType.H3
        case BlockType.H4:
            return HtmlTagType.H4
        case BlockType.H5:
            return HtmlTagType.H5
        case BlockType.H6:
            return HtmlTagType.H6
        case BlockType.CODE:
            return HtmlTagType.CODE
        case BlockType.QUOTE:
            return HtmlTagType.QUOTE
        case BlockType.UL:
            return HtmlTagType.UL
        case BlockType.OL:
            return HtmlTagType.OL
    raise ValueError(f"Unsupported block type: {block_type}")


def text_parser(block_text: str, type: BlockType) -> list[HTMLNode]:
    nodes_list: list[HTMLNode] = []

    if type == BlockType.OL:
        lines = block_text.split("\n")
        for line in lines:
            if not line:
                continue
            modified_line = re.sub(r"^\d+\.\s+", "", line)
            block_children_html_nodes = inline_conversion(modified_line)
            nodes_list.append(ParentNode(tag="li", children=block_children_html_nodes))
        return nodes_list

    if type == BlockType.UL:
        lines = block_text.split("\n")

        for line in lines:
            if not line:
                continue
            modified_line = re.sub(r"^-\s+", "", line)
            block_children_html_nodes = inline_conversion(modified_line)
            nodes_list.append(ParentNode(tag="li", children=block_children_html_nodes))
        return nodes_list

    if type == BlockType.PARA:
        modified_line = re.sub(r"[\r\n]", " ", block_text)
        block_children_html_nodes = inline_conversion(modified_line)
        # nodes_list.append(ParentNode(tag="li", children=block_children_html_nodes))
        return block_children_html_nodes

    if type == BlockType.QUOTE:
        lines = block_text.split("\n")
        cleaned: list[str] = []
        for line in lines:
            if not line.strip():
                continue
            cleaned.append(re.sub(r"^>\s?", "", line))
        joined = " ".join(cleaned)  # "quote" + " " + "with..."
        return inline_conversion(joined)

        return nodes_list

    if type in [
        BlockType.H1,
        BlockType.H2,
        BlockType.H3,
        BlockType.H4,
        BlockType.H5,
        BlockType.H6,
    ]:

        modified_line = re.sub(r"^#+\s*", "", block_text)
        block_children_html_nodes = inline_conversion(modified_line)

        return block_children_html_nodes

    return []


def inline_conversion(line: str) -> list[HTMLNode]:
    block_text_nodes = text_to_textnodes(line)
    block_children_html_nodes = list(map(text_node_to_html_node, block_text_nodes))
    return block_children_html_nodes


def _reassemble_fences(blocks: list[str]) -> list[str]:
    merged: list[str] = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        is_opener = b.strip().startswith("```")
        is_complete = re.match(r"^```\n[\s\S]*```$", b) is not None
        if is_opener and not is_complete:
            parts = [b]
            j = i + 1
            while j < len(blocks):
                parts.append(blocks[j])
                if blocks[j].strip().endswith("```"):
                    break
                j += 1
            merged.append("\n\n".join(parts))
            i = j + 1
        else:
            merged.append(b)
            i += 1
    return merged


def extract_code_content(block: str) -> str:
    """Return raw text inside a fenced code block, without inline parsing.

    Input looks like "```\\ncode\\n```" or "```python\\ncode\\n```".
    Surrounding blank lines are normalized to a single trailing newline,
    e.g. "```\\n\\ncode\\n\\n```" -> "code\\n".
    """
    lines = block.strip().split("\n")

    # First line is the opening fence (``` or ```lang), drop it.
    code_lines = lines[1:] if len(lines) > 1 else []

    # Last line should be the closing fence, drop it if present.
    if code_lines and code_lines[-1].strip() == "```":
        code_lines = code_lines[:-1]

    content = "\n".join(code_lines).strip("\n")
    return f"{content}\n" if content else ""


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = _reassemble_fences(markdown_to_blocks(markdown))
    block_wise_html_nodes: list[HTMLNode] = []

    for block in blocks:
        block_type = block_to_block_type(block)
        tag = mk_type_to_html_tag(block_type)

        if block_type == BlockType.CODE:
            # Code blocks preserve raw text, so skip inline markdown parsing.
            code_text = extract_code_content(block)
            code_text_node = TextNode(code_text, TextType.CODE)
            code_html_node = text_node_to_html_node(code_text_node)
            html_node = ParentNode(tag=tag.value, children=[code_html_node])
            block_wise_html_nodes.append(html_node)

        elif block_type == BlockType.OL or block_type == BlockType.UL:
            block_children_html_nodes = text_parser(block, block_type)
            html_node = ParentNode(tag=tag.value, children=block_children_html_nodes)
            block_wise_html_nodes.append(html_node)

        # paragraph, headings, quote
        else:
            block_children_html_nodes = text_parser(block, block_type)
            html_node = ParentNode(tag=tag.value, children=block_children_html_nodes)
            block_wise_html_nodes.append(html_node)

    div_element = ParentNode(tag="div", children=block_wise_html_nodes)

    return div_element

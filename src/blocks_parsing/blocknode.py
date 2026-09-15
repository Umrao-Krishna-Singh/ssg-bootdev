from enum import Enum
import re


class BlockType(Enum):
    PARA = "paragraph"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    heading_match = re.match(r"^(#{1,6}) (.+)$", block)

    if heading_match:
        heading_level = len(heading_match.group(1))
        return BlockType(f"h{heading_level}")

    if re.match(r"^```\n[\s\S]*```$", block):
        return BlockType.CODE

    if re.match(r"^(?:> ?.*)(?:\n> ?.*)*$", block):
        return BlockType.QUOTE

    if re.match(r"^- .+(?:\n- .+)*$", block):
        return BlockType.UL

    if re.match(r"^\d+\. .+", block):
        lines = block.split("\n")
        for i, line in enumerate(lines, start=1):
            if not re.match(rf"^{i}\. .+$", line):
                return BlockType.PARA
        return BlockType.OL

    return BlockType.PARA

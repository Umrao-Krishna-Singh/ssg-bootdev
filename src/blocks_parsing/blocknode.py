from enum import Enum
import re


class BlockType(Enum):
    PARA = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING

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

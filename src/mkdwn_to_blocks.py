def markdown_to_blocks(markdown: str) -> list[str]:
    delimiter = "\n\n"

    def strip_blocks(block: str) -> str:
        return block.strip()

    def remove_empty(block: str) -> bool:
        return True if block else False

    blocks = list(filter(remove_empty, map(strip_blocks, markdown.split(delimiter))))

    return blocks

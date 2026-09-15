from .textnode import TextNode, TextType
import re


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text

        if delimiter not in text:
            new_nodes.append(old_node)
            continue

        parts = text.split(delimiter)

        # Even number of parts means an unmatched delimiter
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown syntax: unmatched delimiter "
                f"{delimiter!r} in {text!r}"
            )

        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Outside delimiter
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # inside delimiter
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(mkdown: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", mkdown)


def extract_markdown_links(mkdown: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", mkdown)


# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# print(extract_markdown_images(text))
# [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]


# [(text,href)]
def split_nodes_link_delimiter(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for o_note in old_nodes:
        if o_note.text_type != TextType.TEXT:
            new_nodes.append(o_note)
            continue

        o_text = o_note.get_text()
        links = extract_markdown_links(o_text)

        if not len(links):
            new_nodes.append(TextNode(o_text, TextType.TEXT))
            continue

        index = 0
        for link_pair in links:
            [text, href] = link_pair
            delimiter = f"[{text}]({href})"
            o_text_arr = o_text[index:].split(delimiter)

            first = o_text_arr[0]

            if first:
                new_nodes.append(TextNode(first, TextType.TEXT))

            new_nodes.append(TextNode(text, TextType.LINK, href))
            index += len(first) + len(delimiter)

        remaining = o_text[index:]

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


# [alt,src]
def split_nodes_images_delimiter(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for o_note in old_nodes:
        if o_note.text_type != TextType.TEXT:
            new_nodes.append(o_note)
            continue

        o_text = o_note.get_text()
        images = extract_markdown_images(o_text)

        if not len(images):
            new_nodes.append(TextNode(o_text, TextType.TEXT))
            continue

        index = 0
        for image_pair in images:
            [alt, src] = image_pair
            delimiter = f"![{alt}]({src})"
            o_text_arr = o_text[index:].split(delimiter)
            first = o_text_arr[0]

            if first:
                new_nodes.append(TextNode(first, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, src))
            index += len(first) + len(delimiter)

        remaining = o_text[index:]

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    bold_nodes = split_nodes_delimiter(
        [TextNode(text, TextType.TEXT)], "**", TextType.BOLD
    )
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
    link_nodes = split_nodes_link_delimiter(code_nodes)
    image_nodes = split_nodes_images_delimiter(link_nodes)
    return image_nodes

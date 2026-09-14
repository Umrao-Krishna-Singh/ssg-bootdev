from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_notes: list[TextNode] = []
    for o_note in old_nodes:
        if o_note.get_type() != TextType.TEXT:
            new_notes.append(o_note)
        else:
            o_text = o_note.get_text()
            if not o_text:
                new_notes.append(TextNode("", TextType.TEXT))
                continue
            n_text_arr = o_text.split(delimiter)
            n_notes: list[TextNode] = []

            is_valid = (
                True
                if ((len(o_text) - len("".join(n_text_arr))) / len(delimiter) % 2) == 0
                else False
            )

            if not is_valid:
                raise SyntaxError(
                    f"Invalid use of delimiter: {delimiter} \nClosing delimiter was not found for: {delimiter}"
                )

            if not o_text:
                continue

            o_ptr = 0
            n_ptr = 0

            while o_ptr < len(o_text):

                target = o_text[o_ptr]
                test = None
                if o_ptr + len(delimiter) < len(o_text):
                    test = o_text[o_ptr : o_ptr + 2 * len(delimiter)]
                val = n_text_arr[n_ptr]

                # if ghost elements found at start - skip ghost element
                if o_ptr == 0 and o_text[: len(delimiter)] == delimiter:
                    n_ptr += 1
                    val = n_text_arr[n_ptr]
                    n_notes.append(TextNode(val, text_type))
                    o_ptr += len(val) + (2 * len(delimiter))
                    n_ptr += 1

                # Edge case 'a-b--c-d' with - as delimiter -> creates ghost elements ['a', 'b', '', 'c', 'd'] - do not skip ghost element here
                elif test is not None and test == 2 * delimiter:
                    n_notes.append(TextNode("", text_type))
                    o_ptr += 2 * len(delimiter)
                    n_ptr += 1

                elif target != val[0]:
                    n_notes.append(TextNode(val, text_type))
                    o_ptr += len(val) + (2 * len(delimiter))
                    n_ptr += 1

                else:
                    n_notes.append(TextNode(val, TextType.TEXT))
                    o_ptr += len(val)
                    n_ptr += 1

            new_notes.extend(n_notes)

    return new_notes

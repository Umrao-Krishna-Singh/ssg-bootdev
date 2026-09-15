from textnode_parsing.textnode import TextNode, TextType


def main():
    dummy_text = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(dummy_text)


if __name__ == "__main__":
    main()

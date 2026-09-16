from generator import (
    cp_static_data,
    generate_page,
    generate_pages_recursive,
    public,
    content,
    template_html,
    set_basepath,
)
from os.path import join

from sys import argv

basepath = argv[1] if len(argv) > 1 else "/"


def main():
    set_basepath(basepath)
    cp_static_data()
    content_md = join(content, "index.md")
    public_html = join(public, "index.html")

    generate_page(
        from_path=content_md, template_path=template_html, dest_path=public_html
    )
    generate_pages_recursive()


if __name__ == "__main__":
    main()

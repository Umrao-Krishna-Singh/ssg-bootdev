source = "static"
from os import listdir, mkdir
from os.path import join, abspath, dirname, exists, isfile
from shutil import copy, rmtree
from pathlib import Path
from convert import markdown_to_html_node
import re

# directory where this script lives
script_dir = dirname(abspath(__file__))
public = join(script_dir, "..", "public")
static = join(script_dir, "..", "static")
content = join(script_dir, "..", "content")
root = join(script_dir, "..")


def copy_folder(static_path: str, public_path: str):
    static_map = listdir(static_path)
    if not exists(public_path):
        mkdir(public_path)

    for file in static_map:
        file_src = join(static_path, file)
        file_dest = join(public_path, file)
        if isfile(file_src):
            copy(file_src, file_dest)
        else:
            copy_folder(file_src, file_dest)


def cp_static_data():
    if exists(public) and not isfile(public):
        rmtree(public)

    if not exists(public):
        mkdir(public)

    if exists(static) and not isfile(static):
        copy_folder(static, public)


def extract_title(markdown: str) -> str:
    title = next(
        (heading for heading in markdown.split("\n") if re.match(r"^#[^#]", heading)),
        None,
    )

    if title is None:
        raise SyntaxError("Heading not found - no h1 tags found")

    return title.lstrip("#").strip()


def read_file(file_path: str) -> str:
    if exists(file_path) and isfile(file_path):
        return Path(file_path).read_text(encoding="utf-8")

    raise ValueError(
        f"Can not read file - {file_path}, Either the path does not exist or file_path does not point to a file"
    )


def write_file(file_path: str, content: str):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    Path(file_path).write_text(content, encoding="utf-8")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file_data = read_file(from_path)
    template_data = read_file(template_path)
    html_version = markdown_to_html_node(markdown_file_data).to_html()
    title = extract_title(markdown_file_data)
    modified_template = template_data.replace("{{ Title }}", title)
    modified_template = modified_template.replace("{{ Content }}", html_version)
    write_file(dest_path, modified_template)

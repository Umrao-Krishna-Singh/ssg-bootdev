source = "static"
from os import listdir, mkdir
from os.path import join, abspath, dirname, exists, isfile
from shutil import copy, rmtree
from pathlib import Path
from convert import markdown_to_html_node
import re

public = join("docs")
static = join("static")
content = join("content")
root = join(".")
template_html = join(root, "template.html")
basepath = "/"


def set_basepath(path: str):
    global basepath
    basepath = path


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
    # modified_template = template_data.replace("{{ Title }}", title)
    # modified_template = modified_template.replace("{{ Content }}", html_version)

    modified_template = (
        template_data.replace("{{ Title }}", title)
        .replace("{{ Content }}", html_version)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    write_file(dest_path, modified_template)


def generate_pages_recursive(
    dir_path_content: str = content,
    template_path: str = template_html,
    dest_dir_path: str = public,
):
    if not exists(dir_path_content):
        raise ReferenceError(
            "content folder does not exist - order of operation is botched"
        )

    if not exists(dest_dir_path):
        raise ReferenceError(
            "public folder does not exist - order of operation is botched"
        )

    content_map = listdir(dir_path_content)

    for file in content_map:
        file_src = join(dir_path_content, file)
        file_dest = join(dest_dir_path, file)
        if isfile(file_src):
            generate_page(file_src, template_path, file_dest.replace(".md", ".html"))
        else:
            if not exists(file_dest):
                mkdir(file_dest)
            generate_pages_recursive(file_src, template_path, file_dest)

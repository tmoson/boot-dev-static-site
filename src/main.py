from nodefunctions import markdown_to_html_node, extract_title
from textnode import TextNode, TextType
from os import mkdir, listdir, path, getcwd
from shutil import rmtree, copy


def copy_contents(files: list, from_dir: str, to_dir: str):
    if files == [] or files is None:
        return
    if not path.exists(to_dir):
        mkdir(to_dir)
    current = files.pop()
    current_path = path.join(from_dir, current)
    if path.isfile(current_path):
        print(f"copying {current_path} to {path.join(to_dir, current)}")
        copy(current_path, path.join(to_dir, current))
    else:
        new_subdir = path.join(to_dir, path.basename(current))
        print(f"copying {current_path} directory...")
        new_files = listdir(current_path)
        copy_contents(new_files, current_path, new_subdir)
    copy_contents(files, from_dir, to_dir)


def copy_static_to_public(static: str = "static", public: str = "public"):
    if path.exists(public):
        rmtree(public)
    mkdir(public)
    copy_contents(listdir(static), static, public)
    return


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with (
        open(from_path, "r") as from_file,
        open(template_path, "r") as template,
        open(dest_path, "w") as dest,
    ):
        markdown = from_file.read()
        html = template.read()
        title = extract_title(markdown)
        html_node = markdown_to_html_node(markdown)
        html = html.replace("{{ Title }}", title)
        html = html.replace("{{ Content }}", html_node.to_html())
        dest.write(html)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_path: str):
    if dir_path_content == "" or dir_path_content is None:
        return
    if not path.exists(dest_path):
        mkdir(dest_path)
    for item in listdir(dir_path_content):
        item_path = path.join(dir_path_content, item)
        if path.isfile(item_path) and item_path.endswith(".md"):
            html_item_name = item[:-2] + "html"
            generate_page(
                item_path, template_path, path.join(dest_path, html_item_name)
            )
        else:
            new_dest_subdir = path.join(dest_path, item)
            if not path.exists(new_dest_subdir):
                mkdir(new_dest_subdir)
            generate_pages_recursive(item_path, template_path, new_dest_subdir)


def main():
    current_dir = getcwd()
    static_dir = path.join(current_dir, "static")
    public_dir = path.join(current_dir, "public")
    copy_static_to_public(static_dir, public_dir)
    generate_pages_recursive(
        path.join(current_dir, "content"),
        path.join(current_dir, "template.html"),
        public_dir,
    )


main()

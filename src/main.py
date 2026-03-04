from nodefunctions import markdown_to_html_node
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
        print(f"copying {new_subdir} directory...")
        new_files = listdir(new_subdir)
        copy_contents(new_files, current_path, new_subdir)


def copy_static_to_public(static: str = "static", public: str = "public"):
    public_dir = path.join(getcwd(), public)
    for prev_copy in listdir(public_dir):
        rmtree(path.join(public_dir, prev_copy))
    copy_contents(listdir(static), static, public_dir)
    return


def main():
    static_dir = path.join(getcwd(), "static")
    public_dir = path.join(getcwd(), "public")
    copy_static_to_public(static_dir, public_dir)


main()

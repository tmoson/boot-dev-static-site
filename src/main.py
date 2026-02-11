from textnode import TextNode, TextType
from leafnode import LeafNode
import re


def markdown_to_blocks(markdown: str):
    """
    Return empty list if none,
    else string split at double newline with blanks removed.
    """
    if markdown is None:
        return []
    blocks = []
    split_text = list(filter(None, markdown.split("\n\n")))
    for block in split_text:
        blocks.append(block.strip())
    return blocks


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            return LeafNode(tag=None, value=text_node.text)
    return None


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        split_nodes = str.split(node.text, delimiter)
        start_ind = 0
        num_nodes = len(split_nodes)
        if split_nodes[start_ind] == "":
            ++start_ind
        if num_nodes % 2 == 0 and num_nodes != 0:
            raise Exception("ERROR: missing delimiter")
        for i in range(start_ind, num_nodes):
            if i % 2 == 0:
                if split_nodes[i] == "":
                    continue
                else:
                    new_nodes.append(
                        TextNode(
                            text=split_nodes[i], text_type=node.text_type, url=node.url
                        )
                    )
            else:
                new_nodes.append(
                    TextNode(text=split_nodes[i], text_type=text_type, url=node.url)
                )
    return new_nodes


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.LINK or node.text_type == TextType.IMAGE:
            new_nodes.append(node)
            continue
        links = re.findall(r"!\[(.*?)\]\((.*?)\)", node.text)
        num_imgs = len(links)
        if num_imgs == 0:
            new_nodes.append(node)
            continue
        split_text = list(
            filter(None, node.text.split(f"![{links[0][0]}]({links[0][1]})", 1))
        )
        link_at_start = re.match(r"^!\[(.*?)\]\((.*?)\)", node.text) is not None
        for i in range(0, num_imgs):
            if link_at_start:
                new_nodes.append(
                    TextNode(
                        text=links[i][0], text_type=TextType.IMAGE, url=links[i][1]
                    )
                )
                new_nodes.append(TextNode(split_text[1], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(
                    TextNode(
                        text=links[i][0], text_type=TextType.IMAGE, url=links[i][1]
                    )
                )
            if i < num_imgs - 1:
                link_at_start = (
                    re.match(r"^!\[(.*?)\]\((.*?)\)", split_text[1]) is not None
                )
                split_text = list(
                    filter(
                        None,
                        split_text[1].split(
                            f"![{links[i + 1][0]}]({links[i + 1][1]})", 1
                        ),
                    )
                )
            elif len(split_text) > 1:
                new_nodes.append(TextNode(split_text[1], TextType.TEXT))

    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.LINK or node.text_type == TextType.IMAGE:
            new_nodes.append(node)
            continue
        links = re.findall(r"\[(.*?)\]\((.*?)\)", node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        split_text = list(
            filter(None, node.text.split(f"[{links[0][0]}]({links[0][1]})", 1))
        )
        link_at_start = re.match(r"^\[(.*?)\]\((.*?)\)", node.text) is not None
        num_links = len(links)
        for i in range(0, num_links):
            if link_at_start:
                new_nodes.append(
                    TextNode(text=links[i][0], text_type=TextType.LINK, url=links[i][1])
                )
            else:
                new_nodes.append(TextNode(split_text[0], text_type=TextType.TEXT))
                new_nodes.append(
                    TextNode(text=links[i][0], text_type=TextType.LINK, url=links[i][1])
                )
            if i < num_links - 1:
                link_at_start = (
                    re.match(r"^\[(.*?)\]\((.*?)\)", split_text[1]) is not None
                )
                split_text = list(
                    filter(
                        None,
                        split_text[1].split(
                            f"[{links[i + 1][0]}]({links[i + 1][1]})", 1
                        ),
                    )
                )
            elif len(split_text) > 1:
                new_nodes.append(TextNode(split_text[1], TextType.TEXT))
    return new_nodes


def text_to_text_node(text):
    initial_node = TextNode(text, TextType.TEXT)
    return split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_links(split_nodes_images([initial_node])),
                "**",
                TextType.BOLD,
            ),
            "_",
            TextType.ITALIC,
        ),
        "`",
        TextType.CODE,
    )


def main():
    test_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(test_node)


main()

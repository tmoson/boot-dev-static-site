import re
from .textnode import TextNode, text_to_textnodes

type_heading = "heading"
type_ordered_list = "ordered_list"
type_unordered_list = "unordered_list"
type_paragraph = "paragraph"
type_code = "code"
type_quote = "quote"


def block_to_block_type(block):
    if re.match(r'^#{1,6} ([A-z]|[1-9])+', block) is not None:
        return type_heading
    elif block.startswith("```\n") and block.endswith("\n```"):
        return type_code
    elif block.startswith("1."):
        num = 0
        for line in block.splitlines():
            num += 1
            if re.match(r'^(\d+\.)', line) is None:
                return type_paragraph
            elif int(re.match(r'^(\d+)', line).group(0)) != num:
                return type_paragraph
        return type_ordered_list
    elif block.startswith("* "):
        for line in block.splitlines():
            if not line.startswith("* "):
                return type_paragraph
        return type_unordered_list
    elif block.startswith("- "):
        for line in block.splitlines():
            if not line.startswith("- "):
                return type_paragraph
        return type_unordered_list
    elif block.startswith(">"):
        for line in block.splitlines():
            if not line.startswith(">"):
                return type_paragraph
        return type_quote
    else:
        return type_paragraph
        
def markdown_to_blocks(markdown):
    if markdown is None or markdown == "":
        return None
    blocks = []
    block_text = ""
    for line in markdown.splitlines():
        if line == "":
            if block_text == "":
                continue
            else:
                blocks.append(block_text)
                block_text = ""
                continue
        elif block_text == "":
            block_text = line.strip()
            continue
        block_text += "\n" + line.strip()
    if block_text != "":
        blocks.append(block_text)
    return blocks

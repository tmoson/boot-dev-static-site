import re
from .textnode import TextNode, text_to_textnodes

type_header = "header"
type_list = "list"
type_paragraph = "paragraph"
        
def get_block_type(text: str) -> str:
    match text[0]:
        case "#":
            return type_header + str(len(re.match(r"^(#+)", text).group(0)))
        case "*":
            return type_list
        case _:
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

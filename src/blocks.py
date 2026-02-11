from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "u_list"
    ORDERED_LIST = "o_list"

    def __str__(self):
        return self.value


def block_to_block_type(block: str):
    if re.match(r"^#{1,6} .*", block) is not None:
        return BlockType.HEADING
    if block[0:4] == "```\n" and block[-4:] == "\n```":
        return BlockType.CODE
    if re.match(r"^>.*", block) is not None:
        return BlockType.QUOTE
    lines = block.split("\n")
    if lines[0].strip()[0:2] == "- ":
        for line in lines[1:]:
            if line.strip()[0:2] != "- ":
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif re.match(r"^1\. ", lines[0].strip()) is not None:
        prev_num = 1
        for line in lines[1:]:
            if re.match(rf"^{prev_num + 1}\. ", line.strip()) is None:
                return BlockType.PARAGRAPH
            prev_num += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

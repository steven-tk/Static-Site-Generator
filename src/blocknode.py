from enum import Enum


class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEAD
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    else:
        lines = block.splitlines()

        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE

        if all(line.startswith("- ") for line in lines):
            return BlockType.ULIST

        order_check = True
        for i, line in enumerate(lines, start=1):
            if not line.startswith(f"{i}. "):
                order_check = False
                break
        if order_check:
            return BlockType.OLIST
        
        return BlockType.PARA

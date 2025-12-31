from textnode import TextNode, TextType


def markdown_to_blocks(markdown):
    blocks = []

    for block in markdown.split("\n\n"):
        clean_lines = []
        for line in block.splitlines():
            clean_lines.append(line.strip())
        cleaned = "\n".join(clean_lines)

        if cleaned != "":
            blocks.append(cleaned.strip())

    return blocks


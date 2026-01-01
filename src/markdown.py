from htmlnode import ParentNode, LeafNode, text_node_to_html_node
from blocknode import BlockType, block_to_block_type
from nodesplit import text_to_textnodes


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


def text_to_children(block_text):
    html_nodes = []
    text_nodes = text_to_textnodes(block_text)

    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def text_to_ulist_items(block_text):
    html_nodes = []
    lines = block_text.splitlines()
    for line in lines:
        value = line[2:]
        if value == "":
            continue
        html_nodes.append(LeafNode("li", value.strip(), None))
    return html_nodes


def text_to_olist_items(block_text):
    html_nodes = []
    lines = block_text.splitlines()
    for i, line in enumerate(lines, start=1):
        prefix = f"{i}. "
        if not line.startswith(prefix):
            continue
        value = line[len(prefix):]
        html_nodes.append(LeafNode("li", value.strip(), None))
    return html_nodes


def block_node_to_html_node(block, block_type):
    internal_html = None

    if block_type == BlockType.HEAD:
        i = block.count("#",0,7)
        header = block.lstrip("#")
        internal_html = LeafNode(f"h{i}", header.strip())
    if block_type == BlockType.CODE:
        code = block[3:-3]
        if code.startswith("\n"):
            code = code[1:]
        code_child = LeafNode("code", code)
        internal_html = ParentNode("pre", [code_child])
    if block_type == BlockType.QUOTE:
        text = block.replace("> ", "")
        text = text.replace("\n", " ")
        children = text_to_children(text)
        internal_html = ParentNode("blockquote", children)
    if block_type == BlockType.ULIST:
        children = text_to_ulist_items(block)
        internal_html = ParentNode("ul", children)
    if block_type == BlockType.OLIST: # fix
        children = text_to_olist_items(block)
        internal_html = ParentNode("ol", children)
    if block_type == BlockType.PARA:
        text = block.replace("\n", " ")
        children = text_to_children(text)
        internal_html = ParentNode("p", children)
    return internal_html


def markdown_to_html_node(markdown):
    if markdown == "":
        return ParentNode("div", [])
    children = []

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        internal_node = block_node_to_html_node(block, block_type)

        children.append(internal_node)


    div = ParentNode("div", children)
    return div

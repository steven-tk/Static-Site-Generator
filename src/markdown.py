from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
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


def block_node_to_html_node(block, block_type):
    internal_html = None

    if block_type == BlockType.HEAD:
        i = block.count("#",0,7)
        header = block.lstrip("#")
        node_text = text_to_children(header.strip())
        internal_html = LeafNode(f"h{i}", node_text)
    if block_type == BlockType.CODE:
        code = block.strip("```")
        if code.startswith("\n"):
            code = code[1:]
        code_child = LeafNode("code", code)
        internal_html = ParentNode("pre", [code_child])
    if block_type == BlockType.QUOTE:
        children = text_to_children(block)
        internal_html = ParentNode("blockquote", children)
    if block_type == BlockType.ULIST:
        children = text_to_children(block)
        internal_html = ParentNode("ul", children)
    if block_type == BlockType.OLIST:
        children = text_to_children(block)
        internal_html = ParentNode("ol", children)
    if block_type == BlockType.PARA:
        text = block.replace("\n", " ")
        children = text_to_children(text)
        internal_html = ParentNode("p", children)
    return internal_html


def text_to_children(block_text):
    text_nodes = text_to_textnodes(block_text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def markdown_to_html_node(markdown):
    children = []

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        internal_node = block_node_to_html_node(block, block_type)

        children.append(internal_node)


    div = ParentNode("div", children)
    return div


# text_to_textnodes(text)

""" 
-> parent HTMLNode
    -> contain many child HTMLNodes

FYI: I created an additional 8 helper functions to keep my code neat and easy to understand, 
because there's a lot of logic necessary for markdown_to_html_node. 
I don't want to give you my exact functions because I want you to do this from scratch. 
However, I'll give you the basic order of operations:


    - Based on the type of block, create a new HTMLNode with the proper data
    - Assign the proper child HTMLNode objects to the block node.
    I created a shared text_to_children(text) function that works for all block types.
    It takes a string of text and returns a list of HTMLNodes that represent the inline markdown
    using previously created functions (think TextNode -> HTMLNode).
    - The "code" block is a bit of a special case: it should not do any inline markdown parsing of its children.
    I didn't use my text_to_children function for this block type, I manually made a TextNode and used text_node_to_html_node.
- Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.

- Remember Tests
"""
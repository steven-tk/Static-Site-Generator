import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown syntax")

        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part != "":
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"""
        !\[          # literal '!['
        ([^\[\]]*)   # alt text
        \]           # closing bracket
        \(           # opening parenthesis
        ([^\(\)]*)   # URL
        \)           # closing parenthesis
    """, text, re.VERBOSE)
    return matches
# e.g. [("Link1", "url1"), ("Link2", "url2")] for two


def extract_markdown_links(text):
    matches = re.findall(r"""
        (?<!!)       # no '!' in front
        \[           # literal '['
        ([^\[\]]*)   # alt text
        \]           # closing bracket
        \(           # opening parenthesis
        ([^\(\)]*)   # URL
        \)           # closing parenthesis
    """, text, re.VERBOSE)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        while text != "":
            
            data_list = extract_markdown_images(text)
            if not data_list:
                new_nodes.append(TextNode(text, TextType.TEXT))
                break

            alt, link = data_list[0]
            parts = text.split(f"![{alt}]({link})", 1)

            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, link))

            text = str(parts[1])

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        while text != "":
            
            data_list = extract_markdown_links(text)
            if not data_list:
                new_nodes.append(TextNode(text, TextType.TEXT))
                break

            alt, link = data_list[0]
            parts = text.split(f"[{alt}]({link})", 1)

            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, link))

            text = str(parts[1])

    return new_nodes


def text_to_textnodes(text):
    original_node = [TextNode(text, TextType.TEXT)]

    bold_split = split_nodes_delimiter(original_node, "**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
    code_split = split_nodes_delimiter(italic_split, "`", TextType.CODE)
    image_split = split_nodes_image(code_split)
    link_split = split_nodes_link(image_split)

    return link_split


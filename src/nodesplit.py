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


# Old Version
""" def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        split_node = []
        if node.text_type != TextType.TEXT:
            result.append(node)
        
        
        if node.text.count(delimiter) // 2 == 0 and node.text.count(delimiter) > 2:
            raise Exception("Multiple Markdown elements of the same type")

        if node.text.count(delimiter) != 2:
            raise Exception("Invalid Markdown syntax")

        split_node = node.text.split(delimiter)
        front = TextNode(split_node[0], TextType.TEXT)
        nested = TextNode(split_node[1], text_type)
        end = TextNode(split_node[2], TextType.TEXT)

        new_nodes = [front, nested, end]
        result.extend(new_nodes)
    print(result)
    return result """


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



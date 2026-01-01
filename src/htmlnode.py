from textnode import TextNode, TextType

class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        if not self.props:
            return ""
        parts = []
        for key, value in self.props.items():
            parts.append(f'{key}="{value}"')
        return " " + " ".join(parts)

    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)


    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        child_list = []
        for child in self.children:
            child_list.append(child.to_html())
        return f'<{self.tag}{self.props_to_html()}>{"".join(child_list)}</{self.tag}>'



def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        tag = None
        value = text_node.text
        props = None
    elif text_node.text_type == TextType.BOLD:
        tag = "b"
        value = text_node.text
        props = None
    elif text_node.text_type == TextType.ITALIC:
        tag = "i"
        value = text_node.text
        props = None
    elif text_node.text_type == TextType.CODE:
        tag = "code"
        value = text_node.text
        props = None
    elif text_node.text_type == TextType.LINK:
        tag = "a"
        value = text_node.text
        props = {
            "href": text_node.url,
            "target": "_blank",
        }
    elif text_node.text_type == TextType.IMAGE:
        tag = "img"
        value = ""
        props = {
            "src": text_node.url,
            "alt": text_node.text,
        }
    else:
        raise Exception("Not a valid TextType")
    new_leaf = LeafNode(tag, value, props)
    return new_leaf

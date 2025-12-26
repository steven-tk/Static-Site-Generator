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
        if not self.value:
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
    if text_node.text_type not in TextType:
        raise Exception("Not a valid TextType")
    else:
        value = text_node.text

        if text_node.text_type == TextType.TEXT:
            tag = "p"
        if text_node.text_type == TextType.BOLD:
            tag = "b"
        if text_node.text_type == TextType.ITALIC:
            tag = "i"
        if text_node.text_type == TextType.CODE:
            tag = "code"
        if text_node.text_type == TextType.LINK:
            tag = "a"
            props = text_node.url
            # <a href="https://www.google.com">link</a>
        if text_node.text_type == TextType.IMAGE:
            tag = "img"
            props = text_node.url
            # <img src="url/of/image.jpg" alt="Description of image" />

        new_leaf = LeafNode(tag, value, None, props)
        return new_leaf
    


""" 
example dict
{
    "href": "https://www.google.com",
    "target": "_blank",
}
 """

""" 
It should handle each type of the TextType enum. 
If it gets a TextNode that is none of those types, it should raise an exception.
Otherwise, it should return a new LeafNode object.


TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
TextType.BOLD: This should return a LeafNode with a "b" tag and the text
TextType.ITALIC: "i" tag, text
TextType.CODE: "code" tag, text
TextType.LINK: "a" tag, anchor text, and "href" prop
TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
 """

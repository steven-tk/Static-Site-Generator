from textnode import TextNode, TextType
from htmlnode import HTMLNode
from nodesplit import text_to_textnodes


def main():
    print(f"starting...")

    test = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(test))


    """ test_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    test_htmlnode = HTMLNode("this", "is", "a test")
    print(test_node) """



if __name__ == "__main__":
    main()


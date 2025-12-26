from textnode import TextNode, TextType
from htmlnode import HTMLNode


def main():
    print(f"starting...")

    test_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    test_htmlnode = HTMLNode("this", "is", "a test")

    print(test_node)



if __name__ == "__main__":
    main()

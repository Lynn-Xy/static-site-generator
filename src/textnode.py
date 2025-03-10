from enum import Enum
from htmlnode import HTMLNode, LeafNode

class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    IMAGE_TEXT = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):
        if self.url == other_node.url and self.text_type == other_node.text_type and self.text == other_node.text:
            return True

    def __repr__(self):
        print(f"TextNode({self.text}, {self.text_type}, {self.url})")

def textnode_to_htmlnode(textnode):
    match textnode.text_type:
        case TextType.NORMAL_TEXT:
            return LeafNode(tag=None, value=textnode.text, props=None)
        case TextType.BOLD_TEXT:
            return LeafNode(tag="b", value=textnode.text, props=None)
        case TextType.ITALIC_CASE:
            return LeafNode(tag="i", value=textnode.text, props=None)
        case TextType.CODE_TEXT:
            return LeafNode(tag="code", value=textnode.text, props=None)
        case TextType.LINK_TEXT:
            return LeafNode(tag="a", value=textnode.text, props={href:"https://boot.dev"})
        case TextType.IMAGE_TEXT:
            return LeafNode(tag="img", value="", props=textnode.props)
        case _:
            raise Exception("invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            results.append(node)
            continue
        text = node.text
        start_idx = text.find(delimiter)
        if start_idx == -1:
            results.append(node)
            continue
        end_idx = text.find(delimiter, start_idx + len(delimiter))
        if end_idx == -1:
            raise Exception(f"No closing delimiter found for '{delimiter}'")
        pre = text[:start_idx]
        inner = text[start_idx + len(delimiter):end_idx]
        post = text[end_idx + len(delimiter):]
        if pre:
            results.append(TextNode(f"{pre}", TextType.NORMAL_TEXT))
        if inner:
            results.append(TextNode(f"{inner}", text_type))
            if post:
                post_node = TextNode(f"{post}", TextType.NORMAL_TEXT)
                sub_instances = split_nodes_delimiter([post_node], delimiter, text_type)
                results.extend(sub_instances)
        return results

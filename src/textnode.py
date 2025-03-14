from enum import Enum
from htmlnode import HTMLNode, LeafNode
from functions import extract_markdown_images, extract_markdown_links

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
        if self.url:
            return f"TextNode({repr(self.text)}, {repr(self.text_type)}, {repr(self.url)})"
        else:
            return f"TextNode({repr(self.text)}, {repr(self.text_type)})"
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


def split_nodes_image(old_nodes):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            results.append(node)
            continue
        image_data = extract_markdown_images(node.text)
        if not image_data:
            results.append(node)
        else:
            alt_text, image_url = image_data[0]
            image_markdown = f"![{alt_text}]({image_url})"
            parts = node.text.split(image_markdown, 1)
            if parts[0]:
                results.append(TextNode(parts[0], TextType.NORMAL_TEXT))
            results.append(TextNode(alt_text, TextType.IMAGE_TEXT, url=image_url))
            if len(parts) > 1 and parts[1]:
                remaining_node = TextNode(parts[1], TextType.NORMAL_TEXT)
                results.extend(split_nodes_image([remaining_node]))
    return results

def split_nodes_link(old_nodes):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            results.append(node)
            continue
        link_data = extract_markdown_links(node.text)
        if not link_data:
            results.append(node)
        else:
            alt_text, link_url = link_data[0]
            link_markdown = f"[{alt_text}]({link_url})"
            parts = node.text.split(link_markdown, 1)
            if parts[0]:
                results.append(TextNode(parts[0], TextType.NORMAL_TEXT))
                results.append(TextNode(alt_text, TextType.LINK_TEXT, url=link_url))
                if len(parts) > 1 and parts[1]:
                    remaining_node = TextNode(parts[1], TextType.NORMAL_TEXT)
                    results.extend(split_nodes_link([remaining_node]))
    return results

def text_to_textnode(text_string):
    new_node = TextNode(f"{text_string}", TextType.NORMAL_TEXT)
    first_pass = split_nodes_link(split_nodes_image([new_node]))
    second_pass = split_nodes_delimiter(first_pass, "**", TextType.BOLD_TEXT)
    third_pass = split_nodes_delimiter(second_pass, "_", TextType.ITALIC_TEXT)
    final_pass = split_nodes_delimiter(third_pass, "```", TextType.CODE_TEXT)
    return final_pass


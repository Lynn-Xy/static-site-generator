import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block != "":
            new_blocks.append(block.strip())
    return new_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered"

def block_to_block_type(block: str) -> BlockType:
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING

    if re.match(r'^```[\s\S]*?```$', block, re.MULTILINE):
        return BlockType.CODE

    lines = block.split('\n')

    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE

    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST

    if all(re.match(r'^\d+\. ', line) for line in lines):
        numbers = [int(re.match(r'^(\d+)\.', line).group(1)) for line in lines]
        expected = list(range(1, len(numbers) + 1))
        if numbers == expected:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    from textnode import TextType, TextNode, textnode_to_htmlnode, text_to_textnode
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        text_node = text_to_textnode(block)
        html_children = []
        parent_node = None
        parent_tag = ""
        list_children = []
        if block_type == "code":
            html_children = block
        else:
            html_children = [textnode_to_htmlnode(node) for node in text_node]
        html_tag = ""
        html_value = block.strip()
        if block_type == "paragraph":
            html_tag = "p"
        elif block_type == "heading":
            if re.match(r'^#{6} ', block):
                html_tag = "h6"
            elif re.match(r'^#{5} ', block):
                html_tag = "h5"
            elif re.match(r'^#{4} ', block):
                html_tag = "h4"
            elif re.match(r'^#{3} ', block):
                html_tag = "h3"
            elif re.match(r'^#{2} ', block):
                html_tag = "h2"
            elif re.match(r'^#{1} ', block):
                html_tag = "h1"
                html_value = block.lstrip('#').lstrip()
        elif block_type == "code":
            html_tag = "code"
            code_child = HTMLNode(tag=html_tag, value=html_value)
            parent_node = HTMLNode(tag="pre", children=[code_child])
        elif block_type == "quote":
            html_tag = "blockquote"
        elif block_type == "unordered_list":
            for line in block.split("\n"):
                if line.strip():
                    list_children.append(HTMLNode(tag="li", value = line.lstrip("-").strip()))
            parent_tag = "ul"
            parent_node = HTMLNode(tag=parent_tag, children=list_children)
        elif block_type == "ordered_list":
            parent_tag = "ol"
            for line in block.split("\n"):
                if line.strip():
                    list_children.append(HTMLNode(tag="li", value = line.lstrip("-").strip()))
                parent_node = HTMLNode(tag=parent_tag, children=list_children)
        else:
            raise Exception("invalid block_type")
        if parent_node is not None:
            nodes.append(parent_node)
        else:
            nodes.append(HTMLNode(tag=html_tag, value=html_value, children=html_children))
    return HTMLNode(tag="div", children=nodes)

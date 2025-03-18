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

    if re.match(r'^```(\n|.)*?```$', block.strip(), re.DOTALL):
        return BlockType.CODE

    lines = block.split('\n')

    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE

    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST

    if all(re.match(r'^\d+\. ', line) for line in lines):
        numbers = [int(re.match(r'^(\d+)\. ', line).group(1)) for line in lines]
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

        if block_type == BlockType.CODE:
            code_lines = block.split("\n")
            code_content = "\n".join(code_lines[1:-1])
            code_node = textnode_to_htmlnode(TextNode(code_content, text_type=TextType.CODE))

            pre_node = HTMLNode(tag="pre", children=[code_node])
            nodes.append(pre_node)

        elif block_type == BlockType.PARAGRAPH:
            text_nodes = text_to_textnode(block.strip())
            html_children = [textnode_to_htmlnode(node) for node in text_nodes]
            p_node = HTMLNode(tag="p", children=html_children)
            nodes.append(p_node)

        elif block_type == BlockType.HEADING:
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
            text_nodes = text_to_textnode(html_value)
            html_children = [textnode_to_htmlnode(node) for node in text_nodes]
            nodes.append(HTMLNode(tag=html_tag, children=html_children))

        elif block_type == BlockType.QUOTE:
            quote_content = "\n".join([line.lstrip(">").strip() for line in block.split("\n") if line.strip()])
            text_nodes = text_to_textnode(quote_content)
            html_children = [textnode_to_htmlnode(node) for node in text_nodes]
            quote_node = HTMLNode(tag="blockquote", children=html_children)
            nodes.append(quote_node)

        elif block_type == BlockType.UNORDERED_LIST:
            list_items = []
            for line in block.split("\n"):
                if line.strip():
                    item_content = line.lstrip("-").strip()
                    text_nodes = text_to_textnode(item_content)
                    html_children = [textnode_to_htmlnode(node) for node in text_nodes]
                list_items.append(HTMLNode(tag="li", children=html_children))
                list_node = HTMLNode(tag="ul", children=list_items)
                nodes.append(list_node)

        elif block_type == BlockType.ORDERED_LIST:
            list_items = []
            for line in block.split("\n"):
                if line.strip():
                    item_content = re.sub(r'^\d+\.\s*', '', line).strip()
                    text_nodes = text_to_textnode(item_content)
                    html_children = [textnode_to_htmlnode(node) for node in text_nodes]
                    list_items.append(HTMLNode(tag="li", children=html_children))
                    list_node = HTMLNode(tag="ol", children=list_items)
                    nodes.append(list_node)

        else:
            raise Exception("invalid block_type")

    return HTMLNode(tag="div", children=nodes)

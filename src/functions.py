import re
from enum import Enum

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

    if re.match(r'^```[\s\S]*```$', block):
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



from functions import markdown_to_html_node
from htmlnode import HTMLNode

simple_md = "This is **bold** text"
result = markdown_to_html_node(simple_md)
print(result.to_html())

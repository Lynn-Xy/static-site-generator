import unittest

from textnode import TextNode, TextType, textnode_to_htmlnode, split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnode

from functions import extract_markdown_images, extract_markdown_links

class TestTextNode(unittest.TestCase):
    test_node1 = TextNode("This is a **test** node", TextType.BOLD_TEXT)
    test_node2 = TextNode("This is a **test** node", TextType.BOLD_TEXT)
    test_node3 = TextNode("This is _also_ a test node", TextType.ITALIC_TEXT, url="https://boot.dev")

    def test_eq(self):
        self.assertEqual(self.test_node1, self.test_node2)

    def test_uneq(self):
        self.assertNotEqual(self.test_node1, self.test_node3)

    def test_url_is_none(self):
        self.assertIsNone(self.test_node1.url)
        

    def test_url_is_not_none(self):
        self.assertIsNotNone(self.test_node3.url)

    def test_text_to_html(self):
        html_node = textnode_to_htmlnode(self.test_node1)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a **test** node")

    def test_delimiter(self):
        nodes = split_nodes_delimiter([self.test_node1, self.test_node2, self.test_node3], "**", TextType.BOLD_TEXT)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.NORMAL_TEXT), TextNode("image", TextType.IMAGE_TEXT, url="https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", TextType.NORMAL_TEXT), TextNode("second image", TextType.IMAGE_TEXT, url="https://i.imgur.com/3elNhQu.png")], new_nodes)

    def test_split_links(self):
        node = TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with a ", TextType.NORMAL_TEXT), TextNode("link", TextType.LINK_TEXT, url="https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", TextType.NORMAL_TEXT), TextNode("second link", TextType.LINK_TEXT, url="https://i.imgur.com/3elNhQu.png")], new_nodes)

    def test_text_to_textnode(self):
        input_text = "This is **text** with an _italic_ word and a ```code block``` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        old_nodes = [TextNode("This is ", TextType.NORMAL_TEXT), TextNode("text", TextType.BOLD_TEXT), TextNode(" with an ", TextType.NORMAL_TEXT), TextNode("italic", TextType.ITALIC_TEXT), TextNode(" word and a ", TextType.NORMAL_TEXT), TextNode("code block", TextType.CODE_TEXT), TextNode(" and an ", TextType.NORMAL_TEXT), TextNode("obi wan image", TextType.IMAGE_TEXT, url="https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" and a ", TextType.NORMAL_TEXT), TextNode("link", TextType.LINK_TEXT, url="https://boot.dev")]
        new_nodes = text_to_textnode(input_text)
        self.assertEqual(old_nodes, new_nodes)

if __name__ == "__main__":
    unittest.main()

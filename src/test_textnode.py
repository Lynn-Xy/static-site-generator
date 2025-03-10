import unittest

from textnode import TextNode, TextType, textnode_to_htmlnode, split_nodes_delimiter


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

if __name__ == "__main__":
    unittest.main()

import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    test_node1 = TextNode("This is a test node", TextType.BOLD_TEXT)
    test_node2 = TextNode("This is a test node", TextType.BOLD_TEXT)
    test_node3 = TextNode("This is also a test node", TextType.ITALIC_TEXT, url="https://boot.dev")

    def test_eq(self):
        self.assertEqual(self.test_node1, self.test_node2)

    def test_uneq(self):
        self.assertNotEqual(self.test_node1, self.test_node3)

    def test_url_is_none(self):
        self.assertIsNone(self.test_node1.url)
        

    def test_url_is_not_none(self):
        self.assertIsNotNone(self.test_node3.url)


if __name__ == "__main__":
    unittest.main()

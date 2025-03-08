import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    test_node1 = HTMLNode(tag="h1", value="This is a header", children=None, props={"href":"https://boot.dev"})
    test_node2 = HTMLNode(tag="h1", value="This is a header", children=None, props={"href":"https://boot.dev"})
    test_node3 = HTMLNode(tag="p", value="This is normal text", children=[test_node1], props=None)

    def test_eq(self):
        self.assertEqual(self.test_node1, self.test_node2)

    def test_uneq(self):
        self.assertNotEqual(self.test_node1, self.test_node3)

    def test_props_is_none(self):
        self.assertIsNone(self.test_node3.props)                 


class TestLeafNode(TestHTMLNode):
    test_node1 = LeafNode("p", "This is a leafnode")
    test_node2 = LeafNode("p", "This is a leafnode")
    test_node3 = LeafNode("a", "This is also a leafnode", {"href":"https://boot.dev"})

    def test_eq(self):
        self.assertEqual(self.test_node1, self.test_node2)

    def test_uneq(self):
        self.assertNotEqual(self.test_node1, self.test_node3)

    def test_to_html(self):
        self.assertEqual(self.test_node1.to_html(), "<p>This is a leafnode</p>")

if __name__ == "__main__":                                             unittest.main()

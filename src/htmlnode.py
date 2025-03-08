class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Nothing added here yet")

    def props_to_html(self):
        text = f""
        if self.props is not None:
            for i in self.props:
                text = text + " " + f"{i}=" + f"{self.props[i]}"
        return text

    def __repr__(self):
        print(f"{self.tag}" + "\n" + f"{self.value}" + "\n" + f"{self.children}")
        if self.props is not None:
            for i in self.props:
              print(f"{i}:{self.props[i]}")

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=None)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("leafnode must have a value")
        if self.tag is None:
            return f"{self.value}"
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            new = ""
            for i in self.props:
                new = new + f" {i}=\"{self.props[i]}\""
            return f"<{self.tag}{new}>{self.value}</{self.tag}>"

        def __eq__(self, other):
            return self.tag == other.tag and self.value == other.value and self.props == other.props

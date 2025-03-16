class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        if children is None:
            self.children = []
        elif isinstance(children, list):
            self.children = children
        else:
            self.children = [children]
        self.props = props

    def to_html(self):
        if self.tag is None:
            return ""
        props_html = ""
        if self.props is not None:
            for key, value in self.props.items():
                props_html += f' {key}="{value}"'
        if self.value is None and not self.children:
            return f"<{self.tag}{props_html}></{self.tag}>"
        children_html = ""
        if self.children:
            for child in self.children:
                children_html += child.to_html()
        if self.value is None:
            return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"
        else:
            return f"<{self.tag}{props_html}>{self.value}{children_html}</{self.tag}>"

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


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("parentnode must have a tag")
        if self.children is None:
            raise ValueError("parentnode must have children")
        child_text = ""
        for i in self.children:
            child_text += i.to_html()
        new = f"<{self.tag}{self.props_to_html()}>{child_text}</{self.tag}>"
        return new

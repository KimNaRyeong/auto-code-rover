Here is the reproducer script:

```python
import sphinx
from docutils import nodes, utils

def setup(app):
    app.add_node(KbdNode)

class KbdNode(nodes.Element):
    def __init__(self, *children, **kwargs):
        super().__init__(**kwargs)
        self.children = children

    def get_text(self):
        text = ''
        for child in self.children:
            if isinstance(child, nodes.TextElement):
                text += child.astext()
            elif isinstance(child, KbdNode):
                text += '<kbd class="kbd docutils literal notranslate">'
                text += child.get_text()
                text += '</kbd>'
            else:
                raise AssertionError("Unexpected node type")
        return text

def main():
    sphinx.setup()

    try:
        doc = nodes.document()
        root_node = nodes.document()
        doc.append(root_node)

        kbd_node1 = KbdNode(nodes.Text('A'))
        kbd_node2 = KbdNode(nodes.Text('Shift+X'))

        root_node.append(kbd_node1)
        root_node.append(nodes.paragraph())
        root_node.append(kbd_node2)

        sphinx.builder.Builder().write_doc(doc, 'test')
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    main()
```

This script sets up a custom node class `KbdNode` that represents the `<kbd>` element. It then creates two instances of this node and appends them to a document node, which is then written to an HTML file using Sphinx's builder.

If the issue is present, the script should raise an `AssertionError`.
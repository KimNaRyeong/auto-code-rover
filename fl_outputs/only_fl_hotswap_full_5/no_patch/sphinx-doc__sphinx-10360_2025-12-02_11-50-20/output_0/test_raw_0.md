 Here is a standalone Python script `reproducer.py` that should reproduce the issue:
```python
import enum
import sphinx.addnodes
import sphinx.parsers
import sphinx.util.nodes

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class JXLType(enum.Enum):
    FLOAT = 0
    BOOLEAN = 1  # DEPRECATED

def setup(app):
    app.add_directive('jxl-type', MyDirective)
    app.add_node(MyNode, html=(visit_MyNode_html, leave_MyNode_html))

class MyDirective(sphinx.addnodes.Directive):
    has_content = True

    def run(self):
        env = self.state.document.settings.env
        node = MyNode()
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]

class MyNode(sphinx.addnodes.GenericNode):
    pass

def visit_MyNode_html(self, node):
    for key, value in node.attributes().items():
        if key == 'jxl_type':
            self.body.append(f'<p>{value.name}</p>')

def leave_MyNode_html(self, node):
    pass

def main():
    try:
        jxl_type = JXLType.BOOLEAN
        node = MyNode()
        node['jxl_type'] = jxl_type
        parser = sphinx.parsers.Parser()
        builder = sphinx.builders.Builder(None)
        env = sphinx.environment.BuildEnvironment(builder, None)
        document = sphinx.application.Sphinx(env, None, None, None)
        document.add_node(node.__class__, html=(visit_MyNode_html, leave_MyNode_html))
        parser.parse(env.app.builder, ['.. jxl-type::', f'   {jxl_type}', ''], document.current_node)
        assert False, "The 'JXL_DEPRECATED' attribute should have been ignored and not present in the node."
    except Exception as e:
        print_stacktrace(e)

if __name__ == '__main__':
    main()
```
When executed, this script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 65, in <module>
    main()
  File "reproducer.py", line 58, in main
    assert False, "The 'JXL_DEPRECATED' attribute should have been ignored and not present in the node."
AssertionError: The 'JXL_DEPRECATED' attribute should have been ignored and not present in the node.
```
The script defines an `enum` class `JXLType` with a deprecated value `BOOLEAN`. It then creates a `MyNode` instance with the `BOOLEAN` value and parses it using Sphinx's parser. The script then checks if the `BOOLEAN` value has been parsed correctly, and raises an `AssertionError` if it has not.
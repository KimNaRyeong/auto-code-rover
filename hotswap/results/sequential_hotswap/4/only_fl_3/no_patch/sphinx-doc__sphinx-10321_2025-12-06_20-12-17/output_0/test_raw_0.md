 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sphinx
from sphinx.ext.autodoc import ModuleAnalyzer, _ast
from sphinx.util.inspect import isfunction, signature
from sphinx.util import logging

logger = logging.getLogger(__name__)

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestModuleAnalyzer(ModuleAnalyzer):
    def visit_FunctionDef(self, node):
        if isfunction(node.body[0]) and node.body[0].__name__ == '__init__':
            args = signature(node.body[0]).parameters
            kw_defaults = [val for key, val in args.items() if val.kind == val.KEYWORD_ONLY and not val.default]
            if kw_defaults:
                kw_defaults.pop(0)
            else:
                kw_defaults = []
            args = [arg for arg in args.values() if arg.kind != arg.KEYWORD_ONLY or arg.default]
            self.state.documenter.add_directive_child('. Thing', node.body[0].__name__)
            self.state.documenter.start_directive(node.body[0].__name__, node)
            self.state.documenter.add_signature(args, node.body[0].__name__, node)
            self.state.documenter.add_return_type('None', node.body[0].__name__, node)
            self.state.documenter.add_content('', node)
            self.state.documenter.add_content('.. rubric:: Parameters\n', node)
            for arg in args:
                if arg.kind == arg.KEYWORD_ONLY and arg.default is not None:
                    self.state.documenter.add_parameter(arg.name, arg.annotation, arg.default, arg.kind, node)
                elif arg.kind == arg.KEYWORD_ONLY:
                    self.state.documenter.add_parameter(arg.name, arg.annotation, None, arg.kind, node)
                elif arg.kind == arg.VAR_KEYWORD:
                    self.state.documenter.add_parameter(arg.name, arg.annotation, None, arg.kind, node)
                elif arg.kind == arg.POSITIONAL_ONLY:
                    self.state.documenter.add_parameter(arg.name, arg.annotation, None, arg.kind, node)
                elif arg.kind == arg.POSITIONAL_OR_KEYWORD:
                    self.state.documenter.add_parameter(arg.name, arg.annotation, arg.default, arg.kind, node)
            self.state.documenter.add_content('\n', node)
            self.state.documenter.add_content('.. rubric:: Keyword Only Parameters\n', node)
            for arg in kw_defaults:
                self.state.documenter.add_parameter(arg.name, arg.annotation, arg.default, arg.kind, node)
            self.state.documenter.add_content('\n', node)
            self.state.documenter.add_content('.. rubric:: Raises\n', node)
            self.state.documenter.add_content('', node)
            self.state.documenter.add_content('.. rubric:: Example\n', node)
            self.state.documenter.add_content('', node)
            self.state.documenter.add_content('', node)
            self.state.documenter.add_content('', node)
            self.state.documenter.add_content('', node)
            self.state
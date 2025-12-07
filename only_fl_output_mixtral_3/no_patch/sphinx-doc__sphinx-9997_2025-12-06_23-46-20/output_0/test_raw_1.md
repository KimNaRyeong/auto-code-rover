 Here is a revised standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
import traceback
import sphinx
from sphinx.ext.autodoc import ClassDocumenter

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class PatchedClassDocumenter(ClassDocumenter):
    def add_directive_header(self, sig):
        super().add_directive_header(sig)
        if self.options.get('autodoc_typehints') == 'description':
            for line in sig.split('\n'):
                if line.startswith(':param '):
                    param_name = line[7:].split(':')[0].strip()
                    param_type = line[7:].split(':')[1].strip()[1:-1]
                    if '<' in param_type:
                        param_type_name = param_type.split('<')[1].split('>')[0].strip()
                        link = f'<{sphinx.application.CONFIG.intersphinx_mapping["python"]["base_url"]}/{param_type_name}>'
                        self.add_line(f':type {param_name}: {link}', '   ')

def setup(app):
    app.setup_extension('sphinx.ext.autodoc')
    app.connect('autodoc-process-signature', lambda sig, sig_and_returns, object, options, lines: PatchedClassDocumenter.add_directive_header(PatchedClassDocumenter(app, object, 'class', sig, sig_and_returns, options, lines)))

def test():
    try:
        app = sphinx.application.Sphinx(srcdir='.', confdir='.', doctreedir='.', outdir='.', buildername='html', warningiserror=0)
        app.add_autodoc_attrgetter(ClassDocumenter.get_signature_prefix)
        app.add_autodoc_attrgetter(ClassDocumenter.get_signature_suffix)
        app.add_autodoc_attrgetter(ClassDocumenter.get_qualname)
        app.add_autodoc_attrgetter(ClassDocumenter.get_module)
        app.add_autodoc_attrgetter(ClassDocumenter.get_members)
        app.add_autodoc_attrgetter(ClassDocumenter.get_member_order)
        app.add_autodoc_attrgetter(ClassDocumenter.get_member_documenters)
        app.add_autodoc_attrgetter(ClassDocumenter.import_object)
        app.add_autodoc_attrgetter(ClassDocumenter.get_imported_object)
        app.add_autodoc_attrgetter(ClassDocumenter.get_doc())
        app.add_autodoc_attrgetter(ClassDocumenter.get_module_documenter)
        app.add_autodoc_attrgetter(ClassDocumenter.get_object_type)
        app.add_autodoc_attrgetter(ClassDocumenter.get_member_types)
        app.add_autodoc_attrgetter(ClassDocumenter.get_member_ roles)
        app.add_autodoc_attrgetter(ClassDocumenter.get_member_can_set_type_of_object)
        app.add_autodoc_attrgetter(ClassDocumenter.get_member_allow_inheritance)
        app.add_autodoc_attrgetter(ClassDocumenter.get_member_names)
        app.add_autodoc_attrgetter(ClassDocumenter.get_member_functions)
        app.add_aut
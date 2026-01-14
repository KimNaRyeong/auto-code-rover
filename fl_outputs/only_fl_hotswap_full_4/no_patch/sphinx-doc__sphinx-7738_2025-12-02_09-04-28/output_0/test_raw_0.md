 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import os
import sys
from docutils.core import publish_string
from docutils.writers.html4css1 import Writer


def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def main():
    # Arrange
    source = '''
.. autoclass:: a.A
    '''

    settings = {
        'input_encoding': 'utf-8',
        'output_encoding': 'utf-8',
        'doctitle_xform': False,
        'halt_level': 5,
        'report_level': 5,
        'debug': True,
        'warningiserror': True,
        'embed_mode': False,
        'traceback': True,
        'generator': 'Docutils 0.16 [http://docutils.sourceforge.net/]',
        'source_link': False,
        'compact_lists': False,
        'universal_application_name': 'Sphinx',
        'initial_header_level': 1,
        'sectnum_xform': 0,
        'sectnum_depth': 0,
        'file_insertion_enabled': False,
        'raw_enabled': False,
        'xml_declaration': None,
        'doctype_declaration': None,
        'math_output': 'MathJax',
        'math_source': 'mathjax',
        'math_number_all': False,
        'math_media': None,
        'math_format': None,
        'math_engine': None,
        'css_files': [],
        'css_dir': './',
        'mathjax_url': 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js',
        'mathjax_config': 'TeX-AMS-MML_HTMLorMML',
        'mathjax_inline': [['$', '$'], ['\\(', '\\)']],
        'mathjax_block': [['$$', '$$'], ['\\[', '\\]']],
        'smart_quotes': True,
        'smart_entities': True,
        'smart_ dash_punctuation': True,
        'smart_quotes_action': 'qde',
        'smart_entities_action': 'escape',
        'container_class': None,
        'container_id': None,
        'title_role': None,
        'title_prefix': '',
        'title_postfix': '',
        'section_prefix': '',
        'section_postfix': '',
        'table_style': None,
        'top_docname': 'index',
        'template_path': [],
        'template_transaction': 0,
        'template_cache': {},
        'directive_suffix': '.so',
        'exception_prefix': '',
        'default_role': None,
        'random': None,
        'record_dependencies': None,
        'record_dependencies_latex': None,
        'file_insertion_enabled': False,
        'raw_enabled': False,
        'compact_lists': False,
        'sectnum_xform': 0,
        'sectnum_depth': 0,
        'initial_header_level': 1,
        'prune': None,
        'epub_basename': None,
        'epub_tocdepth': 3,
        'epub_tocdup': True,
        'epub_tocscope': None,
        'epub_fix_images': False,
        '
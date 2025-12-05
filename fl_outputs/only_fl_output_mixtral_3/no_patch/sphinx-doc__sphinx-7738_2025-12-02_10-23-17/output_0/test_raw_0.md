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
    source = '''\
.. autoclass:: a.A
    '''

    settings = {
        'input_encoding': 'utf-8',
        'output_encoding': 'utf-8',
        'doctitle_xform': 0,
        ' Haloworld_docclass': None,
        'embed_images': True,
        'compound_documents': None,
        'sectsubtitle_xform': 1,
        'file_insertion_enabled': False,
        'raw_enabled': False,
        'literal_block_enabled': False,
        'doctest_enabled': False,
        'admonition_enabled': False,
        'smart_quotes': False,
        'smartquotes_action': 'none',
        'smartquotes_excludes': ('code', 'literal', 'math', 'pre', 'listing'),
        'highlight_language': 'python3',
        'highlight_options': {},
        'template': '',
        'title': None,
        'subtitle': None,
        'author': None,
        'date': None,
        'release': None,
        'version': None,
        'copyright': None,
        'canonical_url': None,
        'directionality': None,
        'language': None,
        'source_link': None,
        'source_link_suffix': '.',
        'html_math_method': None,
        'css_files': [],
        'math_number_all': False,
        'math_number_density': 0.02,
        'math_media': {'text/html': 'mathjax', 'text/plain': 'plain'},
        'mathjax_options': {
            'align': 'center',
            'mlaisloaded': False,
            'inline': [
                {'mathml': 'math/tex', 'svg': 'mathjax'},
                {'mathml': 'math/tex', 'svg': 'mathjax'},
            ],
            'block': [
                {'mathml': 'math/tex', 'svg': 'mathjax'},
                {'mathml': 'math/tex', 'svg': 'mathjax'},
            ]
        },
        'mathjax_config': '',
        'mathjax_url': 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js',
        'mathjax_config_files': [],
        'abbreviation_map': {},
        'guilabel_localabbrev': None,
        'pep_base_url': 'http://www.python.org/dev/peps/pep-02xx/',
        'rfc_base_url': 'http://tools.ietf.org/html/rfc2xxxx',
        'rfc_patversions': (2, 3, 4, 5, 6, 7, 8),
        'option_warn_type': 'deprecated',
        'trim_footnote_reference_space': True,
        'LaTeX_decimal_leading_zero': False,
        'figure_language_filename': True,
        'list_item_indent_first': 0,
        'list_item_indent_compact': -30,
        'list_item_indent_subcompact': -60,
       
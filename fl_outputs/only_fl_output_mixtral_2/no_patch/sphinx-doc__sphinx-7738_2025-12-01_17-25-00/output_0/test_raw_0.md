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
        'doctitle_xform': 0,
        'halt_level': 5,
        'report_level': 5,
        'debug': True,
        'warningiserror': True,
        'embed_stylesheet': False,
        'prune': False,
        'smart_quotes': False,
        'generator': 'Docutils Python 0.16',
        'source_link': False,
        'tab_width': 8,
        'trim_doctest_flags': True,
        'literal_block_width': 79,
        'random_source_prefix': None,
        'pep_base': True,
        'compact_field_lists': True,
        'sectsubtitle_xform': 1,
        'math_output': 'MathJax',
        'math_source': 'MathJax',
        'admonition_title': 'Notes',
        'stylesheet': [],
        'title': 'reproducer',
        'source_parser': 'restructuredtext.parser.Parser',
        'syntax_highlight': 'short',
        'syntax_highlight_rules': [],
        'template': 'template.html',
        'xml_declaration': None,
        'config_section': 'html4css1 writer',
        'embed_images': True,
        'embed_style': True,
        'compact_field_list': None,
        'sectnum_xform': 1,
        'initial_header_level': 1,
        'figure_caption': True,
        'figure_class': 'figure',
        'option_prefix': 'opt',
        'html_prolog': '',
        'html_sidebars': {},
        'mathjax_config': 'TeX-AMS-MML_HTMLorMML',
        'mathjax_script': 'https://cdn.mathjax.org/mathjax/latest/MathJax.js',
        'mathjax_ssl': False,
        'mathjax_process_scripts': None,
        'smart_entities': True,
        'compact_lists': True,
        'table_style': '',
        'task_lists': True,
        'global_docutils_configuration': None,
        'halt_level': 5,
        'random_source_suffix': '.txt',
        'generator': 'Sphinx 3.0.4',
        'template_path': ['_templates'],
        'source_suffix': '.rst',
        'exclude_patterns': [],
        'keep_warnings': False,
        'encoding': 'utf-8',
        'intersphinx_mapping': {},
        'master_doc': 'index',
        'nitpicky': True,
        'smartquotes': False,
        'smartquotes_action': 'disable',
        'smartquotes_excludes': [],
        'smartquotes_lc_strings': [],
        'smartquotes_lc_punctuation': [],
        'smartquotes_rc_strings': [],
        'smartquotes_rc_punctuation': [],
        'smartquotes_upper': False,
       
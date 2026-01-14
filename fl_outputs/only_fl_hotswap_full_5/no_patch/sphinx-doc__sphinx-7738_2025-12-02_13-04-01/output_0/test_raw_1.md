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
        'compact_flat_dict': True,
        'raw_enabled': False,
        'cloak_email_addresses': False,
        'figure_language_filename': False,
        'list_table_col_widths': None,
        'object_description_prefix': ' :',
        'optimize_images': False,
        'trim_footnote_reference_space': True,
        'math_number_all': False,
        'math_eqref_format': r'Eq. (%s)',
        'math_media': None,
        'math_output': 'mathjax',
        'math_source': 'mathjax',
        'mathjax_config': None,
        'mathjax_options': None,
        'mathjax_inline': [r'\(', r'\)'],
        'mathjax_block': [r'\\[', r'\\]'],
        'mathjax_script': r'\n'.join([
            'MathJax.Hub.Config({',
            '    config: ["MMLorHTML.js"],',
            '    jax: ["input/TeX", "output/CommonHTML"],',
            '    TeX: {',
            '        extensions: ["AMSmath.js", "AMSsymbols.js",',
            '                     "noErrors.js", "noUndefined.js"]',
            '    },',
            '    menuSettings: {',
            '        zoom: "Double-Click",',
            '        zoomFactor: 120',
            '    },',
            '    errorSettings: {',
            '        message: ["[math error]"]',
            '    },',
            '    SVG: {',
            '        blacker: 0,',
            '        fontCache: \'global\',',
            '        useGlobalCache: false',
            '    }',
            '});',
            '',
            'if (window.MathJax) {',
            '    MathJax.Hub.Configured();',
            '}',
        ]),
        'mathjax_script_type': 'text/javascript',
        'mathjax_config_depth': 2,
        'mathjax_config_file': None,
        'mathjax_css': None,
        'mathjax_script_ajax': True,
        'mathjax_config_ajax': True,
        'mathjax_config_url': None,
        'mathjax_config_file_url': None,
        'mathjax_css_url': None,
        'manpage_url': None,
        'smart_quotes': True,
        'smart_quotes_action': 'qde',
        'smart_dash': '--',
        'smart_dash_action': 'hard',
        'smart_str_action': 'soft',
        'smart_entities': True,
        'smart_entities_action': 'soft',
        'template_path': [],
        'directive_path': [],
        'embed_
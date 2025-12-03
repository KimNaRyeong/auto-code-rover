 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import os
import shutil
from docutils.writers.html4css1 import Writer as HTMLWriter

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup_ environment(src_dir, build_dir):
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    shutil.copytree(src_dir, build_dir, symlinks=True)

def build_html(src_dir, build_dir):
    builder = HTMLWriter()
    settings = builder.get_settings()
    settings.env.srcdir = src_dir
    settings.env.app.builder.name = 'html'
    settings.env.app.outdir = build_dir
    settings.env.app.srcdir = src_dir
    settings.env.app.config.html_file_suffix = '.html'
    settings.env.app.config.html_theme = 'default'
    settings.env.app.config.html_theme_path = []
    settings.env.app.config.html_static_path = []
    settings.env.app.config.html_extra_path = []
    settings.env.app.config.html_last_updated_fmt = '%b %d, %Y'
    settings.env.app.config.html_use_smartypants = True
    settings.env.app.config.html_smartypants_dash = '_'
    settings.env.app.config.html_smartypants_ quotes = True
    settings.env.app.config.html_search_language = None
    settings.env.app.config.html_search_options = {}
    settings.env.app.config.html_copy_source = False
    settings.env.app.config.nitpicky = False
    settings.env.app.config.nitpick_ignore = []
    settings.env.app.config.source_suffix = ['.rst']
    settings.env.app.config.source_encoding = None
    settings.env.app.config.warning_is_error = False
    settings.env.app.config.intersphinx_mapping = {}
    settings.env.app.config.highlight_language = 'python'
    settings.env.app.config.pygments_style = 'sphinx'
    settings.env.app.config.trim_doctest_flags = True
    settings.env.app.config.suppress_warnings = []
    settings.env.app.config.templates_path = []
    settings.env.app.config.default_role = None
    settings.env.app.config.add_directive = []
    settings.env.app.config.add_role = []
    settings.env.app.config.add_generic_role = []
    settings.env.app.config.add_event = []
    settings.env.app.config.env_picker = None
    settings.env.app.config.needs_sphinx = '1.0'
    settings.env.app.config.numfig = True
    settings.env.app.config.figure_language_filename = True
    settings.env.app.config.figure_numbers = None
    settings.env.app.config.figure_caption_prefix = None
    settings.env.app.config.figure_caption_separator = None
    settings.env.app.config.figure_caption_max = 0
    settings.env.app.config.linkcode_resolve = None
    settings.env.app.config.nitpick_ignore = []
    settings.env.app.
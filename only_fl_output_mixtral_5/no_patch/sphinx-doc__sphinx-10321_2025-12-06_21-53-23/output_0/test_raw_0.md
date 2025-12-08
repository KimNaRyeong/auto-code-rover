 Here's a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sphinx
from sphinx.ext.autodoc import ModuleAnalyzer, _parse_arglist
from sphinx.util.inspect import isfunction, signature
from sphinx.util import docfields


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


def main():
    class Thing:
        def __init__(
                self,
                kw_or_pos_without_default,
                kw_or_pos_with_default=None,
                *args,
                kw_without_default,
                kw_with_default="Foo"
        ):
            pass

    analyzer = ModuleAnalyzer(None, sphinx.application.Sphinx())
    analyzer.connect('autodoc-process-signature', lambda _: None)
    (signature_object,) = analyzer.get_objects([Thing])
    args, varargs, varkw, defaults = signature(signature_object)

    kw_defaults = {}
    for i, (default, _) in enumerate(reversed(list(zip(defaults or [], args[-len(defaults):])))):
        kw_defaults[args[i].name] = default

    kw_only_params = [param for param in args if param.kind == param.VAR_KEYWORD]
    for param in args:
        if param.kind == param.KEYWORD_ONLY and not param.default:
            if kw_only_params and kw_only_params[-1].name == param.name:
                kw_only_params.pop()
            kw_defaults.pop(param.name, None)

    parsed_args = _parse_arglist(inspect.getsource(signature_object))
    for arg in parsed_args:
        if arg.arg in kw_defaults:
            arg.defvalue = docfields.DefaultValue(kw_defaults[arg.arg], arg.lineno)

    assert arg.defvalue.name is not None, "Expected a non-None name for DefaultValue"


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
To reproduce the issue, execute the script with `python3 reproducer.py`. If the issue is fixed, the script should exit without raising an `AssertionError`.

The script creates a `Thing` class with a constructor similar to the one described in the issue. It then uses Sphinx's `ModuleAnalyzer` and `signature` to parse the signature and extract the default values. The script then manually applies the default values to the parsed arguments. The assertion checks if the `name` attribute of the `DefaultValue` object is not `None`. If it is `None`, the script raises an `AssertionError`, indicating the presence of the issue.
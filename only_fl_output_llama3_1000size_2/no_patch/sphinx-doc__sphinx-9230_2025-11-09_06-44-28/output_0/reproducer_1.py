def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        import sphinx
        from docutils.nodes import paragraph

        def my_function(opc_meta: dict[str, str] = None):
            """This is a test function.

            :param opc_meta: (optional)
                opc_meta (dict(str,str)) – (optional)
            """
            pass

        sphinx.setup()
        sphinx.directives.directive(my_function)

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    main()

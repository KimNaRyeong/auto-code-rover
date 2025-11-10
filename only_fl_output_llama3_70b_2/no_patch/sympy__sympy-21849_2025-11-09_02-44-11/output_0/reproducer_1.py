import sympy as sp

def main():
    function = sp.Pow(sp.LambertW(2), 2)

    try:
        print(function._repr_latex_())
    except TypeError as e:
        print_stacktrace(e)
        assert False, "Error occurred when displaying LambertW function"

if __name__ == "__main__":
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

    main()

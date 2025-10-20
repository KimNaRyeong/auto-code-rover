import sympy as sp

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
    k, m, n = sp.symbols('k m n', integer=True)
    sp.init_printing()

    seq = sp.SeqFormula(n**2, (n, 0, sp.oo))
    seq_str = sp.pretty(seq)

    # We expect the square brackets to not be backslash-escaped
    expected_substr = "[0, 1, 4, 9, \\ldots ]"
    # This checks both issues: the presence of backslash-escaped brackets and the correct rendering of \ldots
    if '\\left\\[' in seq_str or '\\right\\]' in seq_str or expected_substr not in seq_str:
        error_message = 'SeqFormula() display issue: backslash-escaped brackets or incorrect sequence rendering.'
        try:
            assert '\\left\\[' not in seq_str and '\\right\\]' not in seq_str and expected_substr in seq_str, error_message
        except AssertionError as e:
            print_stacktrace(e)
            exit(1) # Exit code 1 for a failure state
    else:
        print("No issue detected with SeqFormula display.")

if __name__ == "__main__":
    main()

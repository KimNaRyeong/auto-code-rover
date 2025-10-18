# reproducer.py
from sympy import symbols, I, Lambda, imageset, S
from sympy.sets.sets import EmptySet

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
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    correct_S1_display = "{n + ⅈ⋅(n - 1)⋅(n + 1) │ n ∊ ℤ}"
    correct_in_S1_result = False  # 2 should not be in S1
    correct_in_S1_intersect_Reals_result = False  # 2 should not be in S1 intersected with Reals
    correct_S1_intersect_Reals_display = "{-1, 1}"

    try:
        assert str(S1) == correct_S1_display, f"S1 display mismatch. Expected: {correct_S1_display}, got: {str(S1)}"
        assert (2 in S1) == correct_in_S1_result, f"Incorrect membership check for 2 in S1. Expected: {correct_in_S1_result}, got: {2 in S1}"
        assert (2 in S1.intersect(S.Reals)) == correct_in_S1_intersect_Reals_result, f"Incorrect membership check for 2 in S1 intersect(Reals). Expected: {correct_in_S1_intersect_Reals_result}, got: {2 in S1.intersect(S.Reals)}"
        intersect_result_display = str(S1.intersect(S.Reals))
        assert intersect_result_display == correct_S1_intersect_Reals_display, f"S1 intersect Reals display mismatch. Expected: {correct_S1_intersect_Reals_display}, got: {intersect_result_display}"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()

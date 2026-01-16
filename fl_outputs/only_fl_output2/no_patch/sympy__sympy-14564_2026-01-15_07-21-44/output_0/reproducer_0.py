import sympy as sp
from sympy import S, pi, Interval, Symbol

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
    x = sp.symbols('x')
    y = sp.symbols('y')
    condition = x > 5

    # Verify ConditionSet behavior
    c1 = sp.ConditionSet(x, condition, Interval(1, 7))
    try:
        assert c1.subs(x, 8) == S.EmptySet, "Substitution outside of the interval should result in EmptySet."
    except AssertionError as e:
        print_stacktrace(e)

    c2 = sp.ConditionSet(x, condition, S.Integers)
    try:
        assert c2.subs(x, 2*pi).is_Integer is False, "Substitution not in the base set should not imply base set membership."
    except AssertionError as e:
        print_stacktrace(e)

    c3 = sp.ConditionSet(y, condition, S.Integers)
    # Assumption based on initial understanding, may need correction based on SymPy's design
    try:
        assert c3.subs(x, 4) == S.EmptySet, "Condition not met leads to EmptySet."
    except AssertionError as e:
        print_stacktrace(e)

    try:
        assert not 6 in c3, "Item should not be considered as part of base set without fulfilling condition."
    except TypeError as e:
        print_stacktrace(e)

    try:
        assert 3 not in c3, "Item not satisfying condition should not be in set."
    except TypeError as e:
        print_stacktrace(e)

    # Address incorrect behavior and raise errors to signal presence of issue
    if any([
        c1.subs(x, 8) != S.EmptySet,
        c2.subs(x, 2*pi) == S.Integers,
        c3.subs(x, 4) != S.EmptySet,
        6 in c3,
        3 in c3
    ]):
        raise AssertionError("One or more issues with ConditionSet identified.")

if __name__ == "__main__":
    main()

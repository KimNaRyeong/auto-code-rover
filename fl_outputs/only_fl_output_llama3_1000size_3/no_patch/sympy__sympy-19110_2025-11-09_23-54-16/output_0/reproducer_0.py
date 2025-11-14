import sympy as sp

def main():
    Z = sp.ZeroMatrix(2, 3)
    Ze = Z.as_explicit()
    if not bool(Z) and bool(Ze):
        raise AssertionError("ZeroMatrix should not be falsey")

try:
    main()
except AssertionError as e:
    print_stacktrace(e)
    exit(0)


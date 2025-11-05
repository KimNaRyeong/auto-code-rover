import sympy as sp

def test_piecewise_rewriting():
    try:
        result = sp.Max('a', 'b').rewrite(sp.Piecewise)
        assert False, "Expected AssertionError"
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_piecewise_rewriting()

import sympy

def test_float_constructor():
    try:
        # Try to create a Float with 54 binary digits
        f = sympy.Float(1.0, prec=54)
        assert False, "Expected ValueError or TypeError"
    except (ValueError, TypeError):
        pass
    else:
        raise AssertionError("Float constructor should not allow setting binary precision")

    try:
        # Try to create a Float with 15 decimal digits and 54 binary digits
        f = sympy.Float(1.0, dps=15, prec=54)
        raise AssertionError("Float constructor should not allow setting both decimal and binary precision")
    except TypeError:
        pass

if __name__ == "__main__":
    try:
        test_float_constructor()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

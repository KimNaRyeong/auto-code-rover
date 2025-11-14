from sympy import Interval, FiniteSet

def test_interval():
    interval_str = str(Interval(0, 1))
    expected_str = "Interval(0, 1)"
    assert interval_str == expected_str, f"Expected {expected_str}, got {interval_str}"
    print("Interval printing is correct")

def test_finiteset():
    finite_set_str = str(FiniteSet(1, 2, 3))
    expected_str = "FiniteSet(1, 2, 3)"
    assert finite_set_str == expected_str, f"Expected {expected_str}, got {finite_set_str}"
    print("FiniteSet printing is correct")

def main():
    try:
        test_interval()
        test_finiteset()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()

import sympy
from sympy.combinatorics import Partition

def test_partition_printing():
    p1 = Partition([1, 2])
    p2 = Partition({1, 2})

    expected_str_p1 = "Partition({1, 2})"
    expected_str_p2 = "Partition({1, 2})"

    try:
        assert str(p1) == expected_str_p1
        assert str(p2) == expected_str_p2
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_partition_printing()

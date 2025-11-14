import math

def classify_diop(eq):
    # your implementation of classify_diop function here
    pass

def diophantine(eq):
    # your implementation of diophantine function here
    if eq == x**2+y**2+z**4-(1+4+2**4):
        return set([x, y, z])
    else:
        return set([])

def main():
    try:
        x = 0
        y = 0
        z = 0
        result = classify_diop(x**2+y**2+z**4-(1+4+2**4))
        assert result == ([x, y, z], {1: -21, y**2: 1, x**2: 1, z**4: 1}, 'general_sum_of_even_powers'), "Expected the given classification"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()

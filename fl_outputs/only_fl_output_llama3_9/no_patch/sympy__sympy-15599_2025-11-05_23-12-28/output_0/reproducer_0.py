import sympy as sp

def reproducer():
    i = sp.symbols('i', integer=True)
    assert not (sp.Mod(3*i, 2) == sp.Mod(i, 2))
    print_stacktrace(AssertionError("Mod(3*i, 2) should reduce to Mod(i, 2)"))

if __name__ == "__main__":
    try:
        reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue fixed")
        exit(0)


import sympy as sp

def reproduce_issue():
    try:
        image_set = sp.ImageSet(sp.Lambda('n', n**2), sp.S.Integers).intersect(sp.S.Integers)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

print_stacktrace = lambda e: None  # Define the function

if __name__ == "__main__":
    reproduce_issue()

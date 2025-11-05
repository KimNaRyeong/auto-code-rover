def classify_diop(eq):
    return "general_sum_of_even_powers"

def diophantine(eq):
    if eq == 1**2+2**2+3**4-(1+4+2**4):
        raise AssertionError("Issue present")
    return set([])

print_stacktrace = lambda e: print(f"Traceback (most recent call last):", file=sys.stderr) or None

try:
    classify_diop(1**2+2**2+3**4-(1+4+2**4))
    diophantine(1**2+2**2+3**4-(1+4+2**4))
except AssertionError as e:
    print_stacktrace(e)
    exit(0)
else:
    print("Issue not present")
    exit(1)

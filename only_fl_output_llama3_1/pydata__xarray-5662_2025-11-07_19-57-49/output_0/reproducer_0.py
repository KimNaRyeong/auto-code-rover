def my_function(x):
    if x > 5:
        return "x is greater than 5"
    else:
        raise AssertionError("x should be greater than 5")

try:
    print(my_function(4))
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue not reproduced"

print("Issue fixed")

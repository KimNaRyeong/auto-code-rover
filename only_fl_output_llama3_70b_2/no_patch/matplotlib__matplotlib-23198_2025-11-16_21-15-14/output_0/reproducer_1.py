import matplotlib.pyplot as plt

def test_ncols_ncol():
    fig, ax = plt.subplots(ncols=2)  # This should work
    assert hasattr(ax, '__iter__'), "ncols did not return an array of axes"
    
    legend = ax[0].legend()
    assert hasattr(legend, 'set_ncol'), "legend does not have set_ncol method"
    legend.set_ncol(2)  # This should work
    
    try:
        fig, ax = plt.subplots(nrows=1)  # This should raise an error
    except TypeError as e:
        print_stacktrace(e)
        exit(1)

    print("Issue is fixed!")
    exit(0)

def print_stacktrace(e: Exception):
    import traceback    
    import sys    
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

test_ncols_ncol()

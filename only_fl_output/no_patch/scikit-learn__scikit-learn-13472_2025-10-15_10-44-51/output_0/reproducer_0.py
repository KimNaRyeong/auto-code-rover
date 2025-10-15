# reproducer.py

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

def try_issue_reproduction():
    import sklearn
    import sklearn.pipeline
    import sklearn.ensemble
    import sklearn.decomposition
    import sklearn.linear_model
    import numpy as np
    
    # Setup a pipeline as an initial estimator
    init = sklearn.pipeline.make_pipeline(sklearn.decomposition.PCA(), sklearn.linear_model.ElasticNet())

    # Pass the pipeline as an initial estimator to GradientBoostingRegressor
    model = sklearn.ensemble.GradientBoostingRegressor(init=init)
    
    # Prepare data
    x = np.random.rand(12, 3)
    y = np.random.rand(12)
    
    # Try fitting the model, which should raise a TypeError due to signature mismatch if the issue is present
    model.fit(x, y)

try:
    try_issue_reproduction()
except TypeError as e:
    print_stacktrace(e)
    # Raise an AssertionError if a TypeError is caught, indicating the issue is present
    raise AssertionError("The issue is present.")
except Exception as e:
    # For any other exceptions, print the stack trace and raise an AssertionError
    print_stacktrace(e)
    raise AssertionError("An unexpected error occurred.")
else:
    print("No issue found, the issue seems to be fixed.")


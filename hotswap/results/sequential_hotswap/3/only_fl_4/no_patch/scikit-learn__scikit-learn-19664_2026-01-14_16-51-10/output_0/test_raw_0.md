```python
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

def run_test():
    import sklearn
    from scipy.sparse import csr_matrix
    from sklearn.datasets import make_classification
    from sklearn.semi_supervised import LabelPropagation

    print("scikit-learn version:", sklearn.__version__)

    # Dense matrix test (expected to work)
    X_dense, y_dense = make_classification()
    classifier_dense = LabelPropagation(kernel='knn')
    try:
        classifier_dense.fit(X_dense, y_dense)
        y_pred_dense = classifier_dense.predict(X_dense)
    except Exception as e:
        print("Dense matrix test FAILED")
        print_stacktrace(e)
        raise AssertionError("Dense matrix test should not raise an exception")

    # Sparse matrix test (expected to fail without the fix)
    X_sparse, y_sparse = make_classification()
    classifier_sparse = LabelPropagation(kernel='knn')
    try:
        classifier_sparse.fit(csr_matrix(X_sparse), y_sparse)
        y_pred_sparse = classifier_sparse.predict(csr_matrix(X_sparse))
    except Exception as e:
        print("Sparse matrix test FAILED")
        print_stacktrace(e)
        raise e  # Raising the original exception to trigger the error.

    print("Sparse matrix test PASSED")

if __name__ == "__main__":
    try:
        run_test()
        print("Test completed successfully.")
    except AssertionError as e:
        print("An expected failure occurred.")
        print_stacktrace(e)
    except Exception as e:
        print("An unexpected error occurred.")
        print_stacktrace(e)
        exit(1)
    exit(0)
```
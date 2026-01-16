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

def test_idf_setting():
    from sklearn.feature_extraction.text import TfidfTransformer
    
    # Simulate a previously computed TfidfTransformer
    TFtransformer = TfidfTransformer(smooth_idf=False)
    TFtransformer.fit_transform([[0, 1, 2], [2, 0, 0]])

    t = TfidfTransformer()
    t.set_params(**TFtransformer.get_params())
    
    try:
        # Attempt to set idf_ directly (expected to fail in the current state)
        t.idf_ = TFtransformer.idf_
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Setting idf_ is not allowed")
    else:
        assert hasattr(t, 'idf_'), "idf_ attribute not set properly"
        assert (t.idf_ == TFtransformer.idf_).all(), "The idf_ values do not match"

if __name__ == "__main__":
    try:
        test_idf_setting()
    except AssertionError as e:
        print(e)
        raise
    print("All tests passed successfully!")

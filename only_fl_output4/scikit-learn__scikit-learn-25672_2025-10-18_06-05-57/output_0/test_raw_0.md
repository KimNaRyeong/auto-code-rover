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

def test_ndcg_with_binary_relevance_and_single_element():
    from sklearn.metrics import ndcg_score

    # Data setup
    y_true = [[1]]
    y_pred = [[0]]
    
    try:
        # This line should raise ValueError according to the issue
        score = ndcg_score(y_true, y_pred)
        print(f"NDCG Score: {score}")
        # If no error is raised, AssertionError is used to indicate the problem still exists
        raise AssertionError("NDCG score computation with binary relevance and a single element should not succeed.")
    except ValueError as e:
        print_stacktrace(e)
        # Assuming the ValueError is specifically about binary format issue with single element list
        # Check if the error message indicates the specific issue
        assert "binary" in str(e), "The error raised is not related to the binary format issue with single element lists."
        print("The issue is correctly reproduced.")
    except Exception as e:
        # Catching any other unexpected exceptions and directly printing the stack trace
        print("An unexpected error occurred:")
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_ndcg_with_binary_relevance_and_single_element()
```
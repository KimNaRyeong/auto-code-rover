```python
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

def main():
    from sklearn.metrics import ndcg_score

    y_true = [[1]]
    y_pred = [[0]]
    
    try:
        score = ndcg_score(y_true, y_pred)
        print("NDCG score calculated.", score)
        # The issue is not present if a ValueError is not raised.
    except ValueError as e:
        print_stacktrace(e)
        # To match the specific error message reported, we assert for the message.
        assert "Only ('multilabel-indicator', 'continuous-multioutput', 'multiclass-multioutput') formats are supported. Got binary instead" in str(e)
        exit(0)  # Exit with code 0 to indicate the issue is reproduced.

if __name__ == "__main__":
    main()
```
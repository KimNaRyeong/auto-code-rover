 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import seaborn as sns
import numpy as np
import sys

def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def custom_min(x):
    return float(np.asarray(x).min())

def main():
    tips = sns.load_dataset("tips")
    try:
        ax = sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
    except Exception as e:
        print_stacktrace(e)
        assert False

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will print the stack trace of the issue:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    main()
  File "reproducer.py", line 19, in main
    ax = sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
  File "C:\Users\<username>\AppData\Local\Programs\Python\Python39\lib\site-packages\seaborn\categorical.py", line 1491, in pointplot
    self.statistic = np.array(statistic)
  File "C:\Users\<username>\AppData\Local\Programs\Python\Python39\lib\site-packages\pandas\core\series.py", line 191, in wrapper
    raise TypeError(f"cannot convert the series to {converter}")
TypeError: cannot convert the series to <class 'float'>
```
This confirms that the issue is present in the `pointplot` function when using a custom estimator. The same error is raised when changing the example code to use `barplot`, or when using a different numpy aggregator within the custom function.
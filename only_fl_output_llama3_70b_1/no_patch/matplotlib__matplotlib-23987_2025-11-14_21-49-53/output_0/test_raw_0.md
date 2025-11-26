Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import matplotlib.pyplot as plt
import numpy as np

def main():
    a = np.linspace(0, 2 * np.pi, 100)
    b = np.sin(a)
    c = np.cos(a)
    fig, ax = plt.subplots(1, 2, figsize=(8, 2), constrained_layout=False)
    ax[0].plot(a, b)
    ax[1].plot(a, c)

    try:
        plt.subplots_adjust(wspace=0)
    except UserWarning as e:
        print_stacktrace(e)
        raise AssertionError("UserWarning should not be raised")

if __name__ == "__main__":
    main()
```
This script will reproduce the issue and raise an `AssertionError` with a stack trace when the warning is generated. If the issue is fixed, the script will exit with code 0.
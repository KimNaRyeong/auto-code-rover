import numpy as np
import matplotlib.pyplot as plt

def main():
    c = np.full(10, np.nan)

    try:
        plt.scatter(np.ones(10), np.ones(10), c=c)
        plt.show()
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected no warning"

    c = np.full(10, np.nan)

    try:
        plt.scatter(np.ones(10), np.ones(10), c=c)
        plt.show()
    except UserWarning as e:
        print_stacktrace(e)
        assert True, "Expected warning"
    else:
        assert False, "Expected warning"

if __name__ == "__main__":
    main()

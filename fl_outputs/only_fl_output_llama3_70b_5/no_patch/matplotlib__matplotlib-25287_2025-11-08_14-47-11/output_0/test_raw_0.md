Here is the `reproducer.py` file to reproduce the issue:
```python
import matplotlib.pyplot as plt

def main():
    plt.rcParams.update({'ytick.labelcolor': 'red'})
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot([1.01e9, 1.02e9, 1.03e9])

    # Get the offset text
    offset_text = ax.yaxis.offsetText

    # Check if the color is correct
    try:
        assert offset_text.get_color() == 'red'
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
<|start_header_id|>
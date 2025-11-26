Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def update(frame):
    return []

fig, ax = plt.subplots()
plt.plot([1,2,3],[2,4,3])
animation = FuncAnimation(fig, update, frames=iter(range(10)), repeat=False, blit=True, interval=100)
try:
    animation.save("hi.mp4")
except StopIteration as e:
    print_stacktrace(e)
    assert False, "StopIteration raised"

fig2, ax2 = plt.subplots()
ax2.plot([7, 6, 3], [3, 5, 2])
try:
    fig2.savefig("hi.png")
except Exception as e:
    print_stacktrace(e)
    assert False, "Exception raised"
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will exit with code 0 when the issue is fixed.

To run this script, save it to a file named `reproducer.py` in the root directory of your project and execute it using `python3 reproducer.py`.
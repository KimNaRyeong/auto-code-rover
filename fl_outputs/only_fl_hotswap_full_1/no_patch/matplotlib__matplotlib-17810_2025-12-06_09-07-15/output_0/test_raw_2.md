 I apologize for the confusion. The error message `ModuleNotFoundError: No module named 'matplotlib'` suggests that the matplotlib library is not installed in the environment where the script is being executed.

Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def update(frame):
    return []

fig, ax = plt.subplots()
plt.plot([1, 2, 3], [2, 4, 3])
animation = FuncAnimation(fig, update, frames=iter(range(10)), repeat=False, blit=True, interval=100)

try:
    animation.save("hi.mp4")
except Exception as e:
    print_stacktrace(e)

fig2, ax2 = plt.subplots()
ax2.plot([7, 6, 3], [3, 5, 2])
try:
    fig2.savefig("hi.png")
except Exception as e:
    print_stacktrace(e)
```
This script uses the provided `print_stacktrace` function to print the stack trace when the `StopIteration` error is raised. The script should reproduce the issue and print the stack trace when run with the command `python3 reproducer.py`. The output should match the one provided in the issue description.

Please make sure that the matplotlib library is installed in the environment where the script is being executed. You can install it using pip or conda, depending on your environment. For example, you can install it using pip with the command `pip install matplotlib`.

Also, I noticed that you are using `conda run` to execute the script. If you are using Anaconda, you can install matplotlib using the following command:
```
conda install matplotlib
```
This should install matplotlib and all its dependencies in the current environment. After that, you can run the script using the command `python3 reproducer.py`.
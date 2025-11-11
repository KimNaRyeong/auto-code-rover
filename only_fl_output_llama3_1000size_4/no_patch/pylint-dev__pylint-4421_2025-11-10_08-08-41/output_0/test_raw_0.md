Here is the reproducer script:

```python
import os
import sys
from pylint.lint import Run

def main():
    # Set up the environment
    venv_path = 'venv'
    if not os.path.exists(venv_path):
        os.makedirs(venv_path)
    activate_this = f'{venv_path}/bin/activate'
    if not os.path.exists(activate_this):
        with open(activate_this, 'w') as f:
            f.write('')

    # Activate the virtual environment
    os.chdir(venv_path)
    with open(activate_this, 'a') as f:
        f.write('if __name__ == "__main__":\n')
        f.write('    python = sys.executable\n')
        f.write('    print(f"Activating {python}...")\n')
        f.write('    os.execl(python, python, "-c", "from venv import *; main()")\n')

    # Install the requirements
    with open('requirements.txt', 'w') as f:
        f.write('pylint\n')
    os.system(f'pip install -r requirements.txt')

    # Run pylint
    try:
        Run(['--rcfile', 'pylintrc', 'demo.py'])
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script sets up a virtual environment, installs the required packages, and then runs pylint with the given configuration. If an exception occurs during the execution of pylint, it prints the stack trace using the provided function and exits with code 1.
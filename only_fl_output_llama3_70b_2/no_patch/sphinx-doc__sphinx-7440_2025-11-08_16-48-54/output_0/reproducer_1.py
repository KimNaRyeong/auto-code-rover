import os
import subprocess

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

try:
    # Clone the repository
    subprocess.run(["git", "clone", "--depth", "1", "https://github.com/phpmyadmin/phpmyadmin.git"], check=True, cwd=os.getcwd())
    
    # Change into the cloned directory
    phpmyadmin_dir = os.path.join(os.getcwd(), "phpmyadmin")
    os.chdir(phpmyadmin_dir)
    
    # Change into the doc directory
    os.chdir("doc")
    
    # Install Sphinx
    subprocess.run(["pip", "install", "Sphinx"], check=True)
    
    # Build the HTML documentation
    subprocess.run(["make", "html"], check=True)
    
    print("Issue not reproduced. The issue might be fixed.")
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Duplicate term 'mysql' and 'MySQL' found")

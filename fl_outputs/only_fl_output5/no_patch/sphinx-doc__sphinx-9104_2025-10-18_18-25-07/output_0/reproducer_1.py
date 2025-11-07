import subprocess
import os
import shutil
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

def check_output_for_warning(output):
    warning_msg = "WARNING: py:class reference target not found: .."
    if warning_msg not in output:
        raise AssertionError(f"Expected warning message '{warning_msg}' not found in Sphinx build output.")

def reproduce_issue():
    repo_url = "https://github.com/altendky/qtrio"
    commit_hash = "661520c1442556016e328169c81c7cd3bdc7f7c3"
    clone_dir = "qtrio_issue_reproduction"

    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)

    subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
    os.chdir(clone_dir)
    subprocess.run(["git", "checkout", commit_hash], check=True)
    
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    pip_exec = ".\\venv\\Scripts\\pip" if os.name == 'nt' else "./venv/bin/pip"
    subprocess.run([pip_exec, "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)
    subprocess.run([pip_exec, "install", ".[pyside2,docs]"], check=True)
    
    os.chdir("docs")
    result = subprocess.run(["make", "html"], capture_output=True, text=True)
    
    check_output_for_warning(result.stdout+result.stderr)

    print("Issue reproduction script completed without detecting the issue.")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
finally:
    # Cleanup and return to the original directory if needed
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    shutil.rmtree("qtrio_issue_reproduction", ignore_errors=True)

import subprocess
import os
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


def setup_project_structure():
    os.makedirs("src/gen", exist_ok=True)
    with open("src/gen/ignored_file.py", "w") as f:
        f.write("# This file should be ignored by pylint\n")

    with open("src/checked_file.py", "w") as f:
        f.write("# This file should be checked by pylint\ninvalid_syntax = \n")

    with open("pyproject.toml", "w") as f:
        f.write("""
[tool.pylint.MASTER]
ignore-paths = [
  # Auto generated
  "^src/gen/.*$",
]
""")


def run_pylint():
    try:
        pylint_executable = [sys.executable, '-m', 'pylint', '--recursive=y', 'src/']
        result = subprocess.run(pylint_executable, capture_output=True, text=True, check=False)
        if "ignored_file.py" in result.stdout or "ignored_file.py" in result.stderr:
            raise AssertionError("The ignored file was checked by pylint")
        if "checked_file.py" not in result.stdout and "checked_file.py" not in result.stderr:
            raise AssertionError("The checked file was unexpectedly ignored by pylint")
        print("Ignored paths are respected, and only targeted files were checked. No issues found.")
    except Exception as e:
        print_stacktrace(e)
        raise


def cleanup_project_structure():
    os.remove("src/gen/ignored_file.py")
    os.remove("src/checked_file.py")
    os.rmdir("src/gen")
    os.rmdir("src")
    os.remove("pyproject.toml")


def main():
    setup_project_structure()
    try:
        run_pylint()
    finally:
        cleanup_project_structure()


if __name__ == "__main__":
    main()

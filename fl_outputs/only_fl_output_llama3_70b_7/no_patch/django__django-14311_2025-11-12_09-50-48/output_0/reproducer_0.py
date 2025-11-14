import os
import sys
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

def test_autoreload():
    # Create a sample module with a dotted name
    os.makedirs('custom_module/pkg', exist_ok=True)
    with open('custom_module/pkg/__init__.py', 'w') as f:
        pass
    with open('custom_module/pkg/submodule.py', 'w') as f:
        f.write("def runserver():\n    print('Running server...')")

    # Run the command that should autoreload
    cmd = [sys.executable, '-m', 'custom_module.pkg.submodule', 'runserver']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Wait for the process to start and print "Running server..."
    output = b''
    while not output.endswith(b'Running server...\n'):
        line = process.stdout.readline()
        output += line
        if not line:
            break

    # Send a signal to trigger autoreload (e.g. SIGHUP on Unix-like systems)
    import signal
    os.kill(process.pid, signal.SIGHUP)

    # Wait for the process to restart and print "Running server..." again
    output = b''
    while not output.endswith(b'Running server...\n'):
        line = process.stdout.readline()
        output += line
        if not line:
            break

    # Check that the process restarted successfully
    assert b'Running server...' in output, "Autoreload failed"

if __name__ == '__main__':
    try:
        test_autoreload()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)

import subprocess
import sys
import tempfile
import venv

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

def test_pylint_quotes_integration():
    # Create a virtual environment
    env_dir = tempfile.mkdtemp()
    venv.create(env_dir, with_pip=True)
    
    # Activate the virtual environment and install required packages
    pip_install_cmd = f'{env_dir}/bin/python -m pip install pylint==2.8.2 pylint-quotes==0.2.1'
    
    try:
        subprocess.check_call(pip_install_cmd.split())
    except subprocess.CalledProcessError as e:
        print("Failed to install packages. Make sure you have internet access and pip works correctly.", file=sys.stderr)
        print_stacktrace(e)
        exit(1)
    
    # Create a sample file to check with pylint
    test_file_path = f"{env_dir}/test_file.py"
    with open(test_file_path, 'w') as test_file:
        test_file.write('foo = "bar"')
    
    # Define pylintrc configuration content
    pylintrc_content = '''
[MASTER]
load-plugins=pylint_quotes
[FORMAT]
single-quotes=yes
    '''

    pylintrc_path = f"{env_dir}/pylintrc"
    with open(pylintrc_path, 'w') as pylintrc_file:
        pylintrc_file.write(pylintrc_content)
    
    # Run pylint with the specified rcfile and file
    pylint_cmd = f'{env_dir}/bin/pylint --rcfile {pylintrc_path} {test_file_path}'
    
    try:
        subprocess.check_output(pylint_cmd.split(), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
        if "TypeError: '<' not supported between instances of 'int' and 'str'" in output:
            print_stacktrace(e)
            assert False, "Issue is still present"
        else:
            # Different error occurred, not expected
            print(output)
            exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    
    print("No issue encountered, exiting with code 0.")
    exit(0)

if __name__ == '__main__':
    test_pylint_quotes_integration()

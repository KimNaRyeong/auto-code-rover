import os
import subprocess
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

def simulate_migration_issue(app_name='testproj'):
    """
    Simulates the migration issue in a controlled environment by creating dummy migrations,
    running the Django migration management command, and catching the expected error.
    """
    
    # Setup dummy migration environment
    migrations_dir = os.path.join(app_name, 'migrations')
    os.makedirs(migrations_dir, exist_ok=True)
    
    # Create dummy migrations
    initial_migration = os.path.join(migrations_dir, '0001_initial.py')
    squashed_migration = os.path.join(migrations_dir, '0001_squashed_0002_thing_age.py')
    second_migration = os.path.join(migrations_dir, '0002_thing_age.py')
    
    for filename in [initial_migration, squashed_migration, second_migration]:
        with open(filename, 'w') as f:
            f.write("# Dummy migration file\n")
    
    try:
        # Attempt to migrate using the specific initial migration script
        cmd = ['python', 'manage.py', 'migrate', app_name, '0001_initial']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Check output for any signs of the issue
        if "CommandError:" in result.stderr or "KeyError:" in result.stderr:
            raise Exception(result.stderr)
    except Exception as e:
        print_stacktrace(e)
        # Raise an assertion error if the KeyError is encountered
        assert False, "Migration issue reproduced successfully."
    finally:
        # Cleanup by removing dummy migrations
        for filename in [initial_migration, squashed_migration, second_migration]:
            os.remove(filename)

if __name__ == "__main__":
    simulate_migration_issue()

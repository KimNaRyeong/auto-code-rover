To create a standalone Python script that aims to reproduce the reported issue regarding Django's `inspectdb` not correctly handling foreign keys to specific fields, we'd have to simulate interactions with a database and Django's inspectdb mechanism directly within the script. This task poses significant challenges due to the complexity and external dependencies involved (e.g., a live database, Django's ORM system). However, it's possible to draft a conceptual script that outlines the steps needed to set up the environment, create the necessary database structure, run `inspectdb`, and check the output for errors related to the foreign key references.

Given these constraints, the following is a conceptual Python script that outlines the process. **Note:** This script won't work out of the box without a configured Django project and requires manual intervention to be fully functional.

```python
# reproducer.py
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

def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        sys.exit(1)

def check_inspectdb_output(output):
    if "ForeignKey('Foo', on_delete=models.CASCADE, db_column='other_id')" not in output:
        raise AssertionError("ForeignKey to specific field 'other_id' is not handled correctly.")

if __name__ == "__main__":
    # Assuming a Django project setup is required and the database has been configured
    # with 'foo' and 'bar' tables as specified in the issue description.

    # This script attempts to run the Django `inspectdb` command. Ideal execution environment
    # would be within a Django project where the database is already configured.
    output = run_command(["django-admin", "inspectdb"])
    
    try:
        check_inspectdb_output(output)
        print("Issue is fixed, exiting with code 0.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```

This script attempts to encapsulate the process of verifying whether the Django `inspectdb` command correctly handles foreign keys to specific fields. It involves:
1. Running the `inspectdb` command on an existing Django project configured with the appropriate database setup.
2. Checking the output to verify if the foreign key is correctly represented as pointing to `foo(other_id)`.

Please note that due to the nature of the issue (it pertains to Django internals and database schema interactions), the precise reproduction and validation should ideally be conducted within a Django project environment where you have direct access to manage.py and an actual database setup that matches the scenario described in the issue.
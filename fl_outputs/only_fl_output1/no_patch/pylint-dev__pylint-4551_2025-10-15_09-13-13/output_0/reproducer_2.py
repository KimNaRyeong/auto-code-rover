import subprocess
import os

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

def generate_uml_and_check_for_type_hints():
    # Python code that should be analyzed
    code = """class C(object):
    def __init__(self, a: str = None):
        self.a = a
"""
    # Write the code to a file
    file_name = "reproducer.py"
    with open(file_name, "w") as file:
        file.write(code)
    
    # Generate UML diagrams using pyreverse
    try:
        output_dir = "uml_diagrams"
        subprocess.run(f"pyreverse -o png -p MyClass {file_name} -a 1 -s 1 -f PUB_ONLY --ignore-none -d {output_dir}", check=True, shell=True)
        
        # Check if the output contains the type hint
        plant_uml_file = f"{output_dir}/classes_MyClass.dot"
        if not os.path.exists(plant_uml_file):
            raise AssertionError("UML diagram file was not generated.")
        
        with open(plant_uml_file, "r") as f:
            content = f.read()
            if ": str" not in content:
                raise AssertionError("Type hint ': str' not found in UML diagram.")
        
        print("Success: Type hint is correctly reflected in UML.")
        
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        raise AssertionError(f"pyreverse command failed: {e}")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    generate_uml_and_check_for_type_hints()

import sys
from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description='Pylint Reproducer')
    parser.add_argument('-v', '--verbose', help='Set verbosity level')

    try:
        args = parser.parse_args()
        if not args.verbose:
            print_stacktrace(AssertionError("Argument expected for short verbose option"))
            sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()

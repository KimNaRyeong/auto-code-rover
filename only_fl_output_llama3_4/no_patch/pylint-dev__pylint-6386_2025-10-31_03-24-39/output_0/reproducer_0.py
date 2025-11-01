import sys
from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description='Pylint reproducer')
    parser.add_argument('-v', '--verbose', help='Verbose mode')

    try:
        args = parser.parse_args()
        if not args.verbose:
            raise AssertionError('Argument expected for short verbose option')
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()

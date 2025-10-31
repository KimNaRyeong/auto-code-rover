import sys
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Verbose mode')
    args, _ = parser.parse_known_args()

    if not hasattr(args, 'verbose') or not isinstance(args.verbose, str):
        raise AssertionError("Argument expected for short verbose option")

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)


import argparse
import sys

from template import MissingVariableError
from templates import library

from parsers import parse_cli_arguments, parse_var

def main() -> None:
    args = parse_cli_arguments()
    
    try:
        template = library.get(args.template)
    except KeyError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    variables: dict[str, str] = {}
    for var_str in args.var:
        try:
            key, value = parse_var(var_str)
        except argparse.ArgumentTypeError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        variables[key] = value

    try:
        result = template.render(**variables)
        print(result)
    except (MissingVariableError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
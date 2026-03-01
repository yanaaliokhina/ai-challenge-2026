import argparse

def parse_cli_arguments() -> dict:
    parser = argparse.ArgumentParser(description="Render a named prompt template.")
    parser.add_argument("--template", required=True, help="Name of the template to render")
    parser.add_argument(
        "--var",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Variable substitution (repeatable)",
    )
    return parser.parse_args()


def parse_var(value: str) -> dict:
    if "=" not in value:
        raise argparse.ArgumentTypeError(f"Variable must be KEY=VALUE format: {value!r}")
    
    key, _, val = value.partition("=")
    return key.strip(), val
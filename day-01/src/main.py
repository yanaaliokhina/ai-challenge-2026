from client.service import LLMRequest, send_request
from utils.cli_parser import parse_arguments

def main() -> None:
    args = parse_arguments()
    
    request = LLMRequest(**vars(args))
    response = send_request(request)

    print(f"\nTokens — input: {response.input_tokens}, output: {response.output_tokens}")


if __name__ == "__main__":
    main()
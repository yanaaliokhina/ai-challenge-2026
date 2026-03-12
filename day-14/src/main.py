from cli_parser import CLIParser
from llm_client import LLMClient
from memory_buffer import MemoryBuffer


def run_chat(buffer: MemoryBuffer, client: LLMClient) -> None:
    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            return

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye.")
            return

        if user_input == "/clear":
            buffer.clear()
            print("[Memory cleared]")
            continue

        if user_input == "/history":
            for msg in buffer.get_messages():
                print(f"[{msg['role']}]: {msg['content']}")
            continue

        buffer.append("user", user_input)
        reply = client.chat(buffer.get_messages(), system=buffer.system_prompt)
        buffer.append("assistant", reply)
        print(f"Assistant: {reply}")


if __name__ == "__main__":
    args = CLIParser().parse_args()
    buffer = MemoryBuffer(max_turns=args.max_turns, system_prompt=args.system)
    client = LLMClient()
    run_chat(buffer, client)

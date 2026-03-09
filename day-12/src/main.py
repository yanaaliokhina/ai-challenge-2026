import sys
from cli_parser import CLIParser
from embedding_client import EmbeddingClient
from chunker import chunk_text
from index_store import load_index, save_index, get_indexed_texts, add_entry, query_index


def run(args) -> None:
    index = load_index(args.index)

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text, chunk_size=args.chunk_size)
        existing_texts = get_indexed_texts(index)
        client = EmbeddingClient()
        new_count = 0

        for chunk in chunks:
            if chunk in existing_texts:
                continue
            embedding = client.embed(chunk)
            add_entry(index, chunk, embedding)
            existing_texts.add(chunk)
            new_count += 1

        save_index(index, args.index)
        print(f"Indexed {new_count} new chunk(s). Total entries: {len(index)}.")

    if args.query:
        if not index:
            print("Index is empty. Run with --file first.")
            sys.exit(1)

        client = EmbeddingClient()
        query_embedding = client.embed(args.query)
        results = query_index(index, query_embedding, top_n=args.top_n)

        print(f"\nTop {len(results)} result(s) for: \"{args.query}\"\n")
        for i, result in enumerate(results, start=1):
            print(f"[{i}] Score: {result['score']:.4f} | {result['text'][:120]!r}")


if __name__ == "__main__":
    args = CLIParser().parse_args()

    if not args.file and not args.query:
        print("Error: provide --file and/or --query.")
        sys.exit(1)

    run(args)

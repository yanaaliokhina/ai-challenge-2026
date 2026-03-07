import sys
from pathlib import Path

from cli_parser import CLIParser
from chunker import chunk_text
from embedder import EmbeddingClient
from retriever import ChunkWithEmbedding, retrieve_top_k
from llm_client import LLMClient


def build_prompt(query: str, ranked_chunks: list) -> str:
    context_parts = [f"[{c['index']}] {c['text']}" for c in ranked_chunks]
    context = "\n\n".join(context_parts)
    return (
        f"Use only the context below to answer the question. "
        f"If the answer is not in the context, say 'I don't know'.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}"
    )


def main() -> None:
    args = CLIParser().parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    text = file_path.read_text(encoding="utf-8")
    if not text.strip():
        print("Error: document is empty", file=sys.stderr)
        sys.exit(1)

    chunks = chunk_text(text, chunk_size=args.chunk_size, overlap=args.overlap)
    if not chunks:
        print("Error: no chunks produced from document", file=sys.stderr)
        sys.exit(1)

    embedder = EmbeddingClient()
    chunk_texts = [c["text"] for c in chunks]
    chunk_embeddings = embedder.embed(chunk_texts)
    query_embedding = embedder.embed([args.query])[0]

    chunk_map: list[ChunkWithEmbedding] = [
        {"index": c["index"], "text": c["text"], "embedding": emb}
        for c, emb in zip(chunks, chunk_embeddings)
    ]
    top_chunks = retrieve_top_k(query_embedding, chunk_map, k=args.top_k)

    if args.verbose:
        print("Retrieved chunks:")
        for c in top_chunks:
            preview = c["text"][:80].replace("\n", " ")
            print(f"  [chunk {c['index']}] similarity={c['score']:.3f} — \"{preview}...\"")
        print()

    prompt = build_prompt(args.query, top_chunks)
    client = LLMClient()
    answer = client.ask(prompt)

    if args.verbose:
        print("Answer:")
    print(answer)


if __name__ == "__main__":
    main()

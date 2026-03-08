"""Tests for prompt construction."""

from src.prompt import build_prompt


class TestBuildPrompt:
    def test_build_prompt_contains_document(self):
        """Verifies that the constructed prompt includes the document content."""
        result = build_prompt("My document text.", "What is this about?")
        assert "My document text." in result

    def test_build_prompt_contains_query(self):
        """Verifies that the constructed prompt includes the user query."""
        result = build_prompt("Some content.", "What methods were used?")
        assert "What methods were used?" in result

    def test_build_prompt_returns_string(self):
        """Verifies that the return type is a string."""
        result = build_prompt("doc", "query")
        assert isinstance(result, str)

    def test_build_prompt_document_before_query(self):
        """Verifies that the document appears before the query in the prompt."""
        doc = "unique_document_marker"
        query = "unique_query_marker"
        result = build_prompt(doc, query)
        assert result.index(doc) < result.index(query)

    def test_build_prompt_empty_document(self):
        """Verifies that an empty document string is handled without error."""
        result = build_prompt("", "What is this?")
        assert "What is this?" in result

    def test_build_prompt_empty_query(self):
        """Verifies that an empty query string is handled without error."""
        result = build_prompt("Some document.", "")
        assert "Some document." in result

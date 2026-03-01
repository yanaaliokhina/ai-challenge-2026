from src.templates import library


def test_translate_template_is_registered():
    """Verifies that the 'translate' predefined template is registered in the library."""
    assert "translate" in library.list_templates()


def test_summarise_template_is_registered():
    """Verifies that the 'summarise' predefined template is registered in the library."""
    assert "summarise" in library.list_templates()


def test_qa_template_is_registered():
    """Verifies that the 'qa' predefined template is registered in the library."""
    assert "qa" in library.list_templates()


def test_all_three_predefined_templates_are_registered():
    """Verifies that all three required predefined templates are registered."""
    names = library.list_templates()
    assert "translate" in names
    assert "summarise" in names
    assert "qa" in names


def test_translate_template_renders_correctly():
    """Verifies that the translate template renders with text and language variables."""
    t = library.get("translate")
    result = t.render(text="Hello", language="French")
    assert "Hello" in result
    assert "French" in result


def test_summarise_template_renders_correctly():
    """Verifies that the summarise template renders with text and num_sentences variables."""
    t = library.get("summarise")
    result = t.render(text="Some long text.", num_sentences="3")
    assert "Some long text." in result
    assert "3" in result


def test_qa_template_renders_correctly():
    """Verifies that the qa template renders with question and context variables."""
    t = library.get("qa")
    result = t.render(question="What is AI?", context="AI is artificial intelligence.")
    assert "What is AI?" in result
    assert "AI is artificial intelligence." in result


def test_translate_template_placeholders():
    """Verifies that the translate template requires exactly text and language placeholders."""
    t = library.get("translate")
    assert t.placeholders == frozenset({"text", "language"})


def test_summarise_template_placeholders():
    """Verifies that the summarise template requires exactly text and num_sentences placeholders."""
    t = library.get("summarise")
    assert t.placeholders == frozenset({"text", "num_sentences"})


def test_qa_template_placeholders():
    """Verifies that the qa template requires exactly question and context placeholders."""
    t = library.get("qa")
    assert t.placeholders == frozenset({"question", "context"})

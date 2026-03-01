import pytest
from src.library import TemplateLibrary
from src.template import PromptTemplate


def test_register_and_get_template():
    """Verifies that a registered template can be retrieved by name."""
    lib = TemplateLibrary()
    t = PromptTemplate("Hello {name}.")
    lib.register("greet", t)
    assert lib.get("greet") is t


def test_get_raises_key_error_for_unknown_template():
    """Verifies that get raises KeyError when the template name is not found."""
    lib = TemplateLibrary()
    with pytest.raises(KeyError):
        lib.get("nonexistent")


def test_list_templates_returns_sorted_names():
    """Verifies that list_templates returns a sorted list of registered template names."""
    lib = TemplateLibrary()
    lib.register("zebra", PromptTemplate("Z {x}"))
    lib.register("apple", PromptTemplate("A {x}"))
    lib.register("mango", PromptTemplate("M {x}"))
    assert lib.list_templates() == ["apple", "mango", "zebra"]


def test_list_templates_empty_when_no_templates_registered():
    """Verifies that list_templates returns an empty list when no templates are registered."""
    lib = TemplateLibrary()
    assert lib.list_templates() == []


def test_register_overwrites_existing_template():
    """Verifies that registering with an existing name overwrites the previous template."""
    lib = TemplateLibrary()
    t1 = PromptTemplate("First {x}")
    t2 = PromptTemplate("Second {x}")
    lib.register("name", t1)
    lib.register("name", t2)
    assert lib.get("name") is t2


def test_list_templates_returns_list_type():
    """Verifies that list_templates returns a list, not another collection type."""
    lib = TemplateLibrary()
    lib.register("a", PromptTemplate("A"))
    result = lib.list_templates()
    assert isinstance(result, list)


def test_get_returns_correct_template_when_multiple_registered():
    """Verifies that get returns the correct template when multiple are registered."""
    lib = TemplateLibrary()
    t1 = PromptTemplate("Template one {x}")
    t2 = PromptTemplate("Template two {y}")
    lib.register("one", t1)
    lib.register("two", t2)
    assert lib.get("one") is t1
    assert lib.get("two") is t2

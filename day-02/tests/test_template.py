import pytest
from src.template import MissingVariableError, PromptTemplate


def test_render_substitutes_all_placeholders():
    """Verifies that render correctly substitutes all placeholders."""
    t = PromptTemplate("Translate {text} into {language}.")
    result = t.render(text="Hello", language="French")
    assert result == "Translate Hello into French."


def test_render_single_placeholder():
    """Verifies that render works with a single placeholder."""
    t = PromptTemplate("Say: {message}")
    result = t.render(message="hello")
    assert result == "Say: hello"


def test_render_with_no_placeholders():
    """Verifies that a template with no placeholders renders with no variables."""
    t = PromptTemplate("Hello world.")
    result = t.render()
    assert result == "Hello world."


def test_render_raises_missing_variable_error_for_single_missing():
    """Verifies that MissingVariableError is raised when one placeholder is not provided."""
    t = PromptTemplate("Hello {name}, you are {age} years old.")
    with pytest.raises(MissingVariableError) as exc_info:
        t.render(name="Alice")
    assert "age" in str(exc_info.value)
    assert "age" in exc_info.value.missing


def test_render_raises_missing_variable_error_listing_all_missing():
    """Verifies that MissingVariableError lists all missing variables, not just the first."""
    t = PromptTemplate("Hello {name}, you are {age} and live in {city}.")
    with pytest.raises(MissingVariableError) as exc_info:
        t.render()
    assert sorted(exc_info.value.missing) == ["age", "city", "name"]


def test_missing_variable_error_has_missing_attribute():
    """Verifies that MissingVariableError exposes a .missing list of variable names."""
    t = PromptTemplate("{a} and {b}")
    with pytest.raises(MissingVariableError) as exc_info:
        t.render(a="1")
    assert exc_info.value.missing == ["b"]


def test_render_raises_value_error_for_extra_variable():
    """Verifies that ValueError is raised when an extra/unused variable is passed."""
    t = PromptTemplate("Hello {name}.")
    with pytest.raises(ValueError) as exc_info:
        t.render(name="Alice", unknown="extra")
    assert "unknown" in str(exc_info.value)


def test_render_raises_value_error_listing_all_extra_variables():
    """Verifies that ValueError message includes all extra variable names."""
    t = PromptTemplate("Hello {name}.")
    with pytest.raises(ValueError) as exc_info:
        t.render(name="Alice", extra1="a", extra2="b")
    error_msg = str(exc_info.value)
    assert "extra1" in error_msg
    assert "extra2" in error_msg


def test_render_raises_value_error_when_extra_passed_to_no_placeholder_template():
    """Verifies that ValueError is raised when variables are given to a placeholder-free template."""
    t = PromptTemplate("Hello world.")
    with pytest.raises(ValueError):
        t.render(extra="value")


def test_placeholders_extracted_correctly():
    """Verifies that placeholder names are parsed correctly from the template string."""
    t = PromptTemplate("Hello {name}, you are {age}.")
    assert t.placeholders == frozenset({"name", "age"})


def test_placeholders_empty_for_no_placeholder_template():
    """Verifies that placeholders returns an empty frozenset for a plain string template."""
    t = PromptTemplate("No placeholders here.")
    assert t.placeholders == frozenset()


def test_placeholders_property_returns_frozenset():
    """Verifies that the placeholders property returns a frozenset type."""
    t = PromptTemplate("{x} and {y}")
    assert isinstance(t.placeholders, frozenset)

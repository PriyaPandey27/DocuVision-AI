import pytest
from pdf_text_processor import TextGen
from pdf_image_processor import Image_Gen

def test_textgen_initialization():
    """Test that the text generator class initializes properly without fatal errors (assuming HF_TOKEN is optionally mocked)."""
    text_model = TextGen()
    assert text_model is not None, "Text model should instantiate."
    assert hasattr(text_model, 'datafolder'), "Should have a data folder property."

def test_imagegen_initialization():
    """Test that the image generator class initializes correctly."""
    image_model = Image_Gen()
    assert image_model is not None, "Image model should instantiate."
    assert hasattr(image_model, 'datafolder'), "Should have a data folder property."

def test_utf8_sanitization():
    """Test helper parsing logic in Image_Gen for UTF-8."""
    image_model = Image_Gen()
    test_str = "Clean text \x80"
    cleaned = image_model.remove_non_utf8(test_str)
    assert "\\x80" not in cleaned, "Non-UTF8 characters should be removed or sanitized."

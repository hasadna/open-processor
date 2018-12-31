"""Testing the integration of our code."""

from i18n import i18n


def test_fields():
    """Testing the fields loading."""
    translator = i18n()

    translator.set_fields({"food": "pizza"})

    assert translator.translate_field("food") == "pizza"
    assert translator.translate_field("pizza") is None


def test_sheets():
    """Testing the fields loading."""
    translator = i18n()

    translator.set_sheets({"food": "pizza"})

    assert translator.translate_sheet("food") == "pizza"
    assert translator.translate_sheet("pizza") is None

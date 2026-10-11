from presentation_api.slides.parser import parse_markdown, parse_slide, split_blockquote_slides
from presentation_api.slides.schemas import Slide


def test_consecutive_quote_lines_form_one_slide():
    text = "> # Title\n>\n> - item\n>   more"
    assert split_blockquote_slides(text) == ["# Title\n\n- item\n  more"]


def test_empty_line_or_narration_starts_new_slide():
    text = "> one\n\n> two\nnarration\n> three"
    assert split_blockquote_slides(text) == ["one", "two", "three"]


def test_lines_outside_quotes_and_in_code_fences_are_ignored():
    text = "# Heading\nnarration\n```\n> not a slide\n```\n> slide"
    assert split_blockquote_slides(text) == ["slide"]


def test_empty_quotes_are_skipped():
    assert split_blockquote_slides(">\n>\n\n> x") == ["x"]


def test_text_slide():
    assert parse_slide("Main title") == Slide(type="text", value="Main title")


def test_image_with_destination_title_and_encoded_angle_target():
    slide = parse_slide("![main: funny image](</Screenshot%20(1).png>)")
    assert slide == Slide(title="funny image", type="image:png", value="Screenshot (1).png")


def test_file_link_with_destination_and_title():
    slide = parse_slide("[main:some code](/test.json)")
    assert slide == Slide(title="some code", type="file:json", value="test.json")


def test_label_without_colon_known_destination():
    slide = parse_slide("[chat](/session.md)")
    assert slide == Slide(type="file:md", destination="chat", value="session.md")


def test_label_without_colon_is_title():
    slide = parse_slide("[some code](/test.json)")
    assert slide == Slide(title="some code", type="file:json", value="test.json")


def test_empty_title_and_empty_label():
    assert parse_slide("[chat:](/a.md)") == Slide(type="file:md", destination="chat", value="a.md")
    assert parse_slide("![](/a.PNG)") == Slide(type="image:png", value="a.PNG")


def test_custom_destination():
    slide = parse_slide("[sidebar: Notes](/notes.md)")
    assert slide == Slide(title="Notes", type="file:md", destination="sidebar", value="notes.md")


def test_link_mixed_with_text_stays_text():
    body = "# Look\n![main: img](/a.png)"
    assert parse_slide(body) == Slide(type="text", value=body)


def test_link_without_extension_or_external_stays_text():
    for body in ("[docs](/Makefile)", "[docs](https://example.com/a.json)"):
        assert parse_slide(body) == Slide(type="text", value=body)


def test_parse_markdown():
    text = "Intro\n\n> Hello\n\n> ![main: pic](</a%20b.png>)\n"
    assert parse_markdown(text) == [
        Slide(type="text", value="Hello"),
        Slide(title="pic", type="image:png", value="a b.png"),
    ]

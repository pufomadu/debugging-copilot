from src.error_parser import parse_error

def test_parse_name_error():
    msg = "NameError: name 'df' is not defined"
    parsed = parse_error(msg)
    assert "NameError" in parsed["labels"]
    assert "df" in parsed["entities"]

def test_parse_key_error():
    msg = "KeyError: 'age'"
    parsed = parse_error(msg)
    assert "KeyError" in parsed["labels"]
    assert "age" in parsed["entities"]

def test_parse_unrecognized_error():
    msg = "Some random message"
    parsed = parse_error(msg)
    assert parsed["labels"] == []

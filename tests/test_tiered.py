from src.tiered_helper import answer

# Concept question tests
def test_tier_1_concept():
    resp = answer("What is SQL?", explicit_request=1)
    assert "tier" in str(resp) or "nudge" in str(resp).lower()

def test_tier_2_concept():
    resp = answer("What is SQL?", explicit_request=2)
    assert "step" in str(resp).lower()

def test_tier_3_concept():
    resp = answer("What is SQL?", explicit_request=3)
    assert "citations" in str(resp).lower() or "example" in str(resp).lower()

def test_tier_4_concept():
    resp = answer("What is SQL?", explicit_request=4)
    assert "code" in str(resp).lower() or "solution" in str(resp).lower()

# Error handling tests
def test_tiered_with_code_snippet():
    code = "print(df.head())"
    resp = answer("NameError: name 'df' is not defined", code_snippet=code, explicit_request=3)
    assert "df" in str(resp)

def test_invalid_tier_defaults():
    resp = answer("What is SQL?", explicit_request=99)
    assert "tier" in str(resp) or isinstance(resp, str)

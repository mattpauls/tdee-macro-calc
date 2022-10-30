import pytest
from tdee_macro_calc.main import check_valid_date

@pytest.mark.parametrize("test_input,expected", [
    ("5/21/1989", True),
    (5.21, False),
    ("5/21", False)
])
def test_check_valid_date(test_input, expected):
    assert check_valid_date(test_input) is expected

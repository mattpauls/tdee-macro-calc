import pytest
import datetime
from tdee_macro_calc.main import convert_date

@pytest.mark.parametrize("test_input,expected",[
    #TODO add more inputs, takes datetime object and converts to string formatted as MM/DD/YYYY
    # if is already a string, returns the string
    ("5/21/89", "5/21/89"),
    (datetime.date(2022, 10, 5), "10/05/2022"),
    (datetime.date(2019, 5, 5), "05/05/2019")
])
# Converts date to a string, formatted as MM/DD/YYYY
def test_convert_date(test_input, expected):
    assert convert_date(test_input) == expected
from tdee_macro_calc.main import check_valid_date

def test_check_valid_date():
    assert check_valid_date("5/21/1989") == True
    assert check_valid_date(5.21) == False
    assert check_valid_date("5/21") == False

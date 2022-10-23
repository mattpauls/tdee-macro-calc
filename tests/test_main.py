import json
from tdee_macro_calc.main import check_data_file

# tmp_path is a pytest fixture (a bit of magic).
# It gets created and 'torn-down' after every unit test.
def test_check_data_files(tmp_path):
    check_data_file(home_dir=tmp_path)
    expected_path = tmp_path / '.tdee' / 'data.json'
    # Ensure that the expected directory+file is created
    assert expected_path.exists()
    # Ensure that the content written to this file is as expected
    raw_content = expected_path.read_text()
    content = json.loads(raw_content)
    assert "user" in content
    assert "tdee" in content
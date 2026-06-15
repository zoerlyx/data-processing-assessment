
import pandas as pd
from unittest.mock import patch, MagicMock  # ← import patch di sini
import pytest
from utils.load import save_to_csv, save_to_google_sheets, save_to_postgresql


# Sample DataFrame untuk testing
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "title": ["T-shirt 2", "Hoodie 3"],
        "price": [1634400.0, 7950080.0],
        "rating": [3.9, 4.8],
        "colors": [3, 3],
        "size": ["M", "L"],
        "gender": ["Women", "Unisex"],
        "timestamp": ["2026-05-01 15:23:03", "2026-05-01 15:23:03"]
    })


# Test save_to_csv
def test_save_to_csv(sample_df, tmp_path):
    csv_path = tmp_path / "products.csv"
    with patch("pandas.DataFrame.to_csv") as mock_csv:
        result = save_to_csv(sample_df)
        assert result == True


# Test save_to_google_sheets
@patch("utils.load.gspread.authorize")
@patch("utils.load.Credentials.from_service_account_file")
def test_save_to_google_sheets(mock_creds, mock_auth, sample_df):

    mock_client = MagicMock()
    mock_auth.return_value = mock_client
    mock_spreadsheet = MagicMock()
    mock_client.open.return_value = mock_spreadsheet
    mock_worksheet = MagicMock()
    mock_spreadsheet.sheet1 = mock_worksheet

    result = save_to_google_sheets(sample_df)
    assert result == True
    mock_worksheet.clear.assert_called_once()
    mock_worksheet.update.assert_called_once()


# Test save_to_postgresql
@patch("utils.load.create_engine")
def test_save_to_postgresql(mock_engine, sample_df):

    mock_conn = MagicMock()
    mock_engine.return_value = mock_conn

    with patch("pandas.DataFrame.to_sql") as mock_sql:
        result = save_to_postgresql(sample_df)
        assert result == True

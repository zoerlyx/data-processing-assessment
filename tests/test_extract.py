
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from utils.extract import extract_product_data, scrape_page, scrape_main


# Test extract_product_data — sukses
def test_extract_product_data_success():
    mock_card = MagicMock()
    mock_card.find.return_value.text.strip.return_value = "T-shirt"
    mock_card.find_all.return_value = [
        MagicMock(text="Rating: 4.5 / 5"),
        MagicMock(text="3 Colors"),
        MagicMock(text="Size: M"),
        MagicMock(text="Gender: Men"),
    ]
    result = extract_product_data(mock_card)
    assert result is not None
    assert result["title"] == "T-shirt"


# test extract_product_data — gagal/exception
def test_extract_product_data_failure():
    mock_card = MagicMock()
    mock_card.find.side_effect = Exception("Error")
    result = extract_product_data(mock_card)
    assert result is None


# test scrape_page — sukses
@patch("utils.extract.requests.get")
def test_scrape_page_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '''
    <html>
        <div class="collection-card">
            <h3 class="product-title">Test Product</h3>
            <span class="price">$10</span>
            <p>4.5 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Men</p>
        </div>
    </html>
    '''
    mock_get.return_value = mock_response
    result = scrape_page(1)
    assert isinstance(result, list)


# test scrape_page gagal request
@patch("utils.extract.requests.get")
def test_scrape_page_failure(mock_get):
    import requests
    mock_get.side_effect = requests.RequestException("Timeout")
    result = scrape_page(1)
    assert result == []


# Test scrape_main
@patch("utils.extract.scrape_page")
def test_scrape_main(mock_scrape_page):
    mock_scrape_page.return_value = [
        {"title": "T-shirt", "price": "$10", "rating": "4.5 / 5",
         "colors": "3 Colors", "size": "Size: M", "gender": "Gender: Men"}
    ]
    result = scrape_main()
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 50


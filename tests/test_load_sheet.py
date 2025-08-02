import sys
import os

# ✅ Tambahkan folder root ke path agar 'utils' bisa dikenali
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load_data.load_sheet import upload_ke_sheet  # gunakan nama fungsi yang benar

class TestLoadSheet(unittest.TestCase):

    @patch("utils.load_data.load_sheet.service_account.Credentials.from_service_account_file")
    @patch("utils.load_data.load_sheet.build")
    def test_load_to_google_sheets_success(self, mock_build, mock_creds):
        mock_creds.return_value = MagicMock()

        mock_sheets = MagicMock()
        mock_build.return_value.spreadsheets.return_value = mock_sheets

        mock_sheets.values().update.return_value.execute.return_value = {"status": "OK"}

        data = {
            "Title": ["Sneakers X"],
            "Price": [160000],
            "Rating": [4.5],
            "Colors": [3],
            "Size": ["M"],
            "Gender": ["Unisex"]
        }
        df = pd.DataFrame(data)

        upload_ke_sheet(df)

        mock_sheets.values().update.assert_called_once()

    @patch("utils.load_data.load_sheet.service_account.Credentials.from_service_account_file")
    @patch("utils.load_data.load_sheet.build")
    def test_load_to_google_sheets_api_error(self, mock_build, mock_creds):
        mock_creds.return_value = MagicMock()

        mock_sheets = MagicMock()
        mock_build.return_value.spreadsheets.return_value = mock_sheets
        mock_sheets.values().update.side_effect = Exception("Google API Error")

        data = {
            "Title": ["Urban Jacket"],
            "Price": [200000],
            "Rating": [4.2],
            "Colors": [2],
            "Size": ["L"],
            "Gender": ["Male"]
        }
        df = pd.DataFrame(data)

        with self.assertLogs(level="ERROR") as log:
            upload_ke_sheet(df)

        self.assertTrue(any("Google API Error" in message for message in log.output))

    @patch("utils.load_data.load_sheet.service_account.Credentials.from_service_account_file")
    @patch("utils.load_data.load_sheet.build")
    def test_load_to_google_sheets_empty_dataframe(self, mock_build, mock_creds):
        mock_creds.return_value = MagicMock()
        mock_build.return_value.spreadsheets.return_value = MagicMock()

        df = pd.DataFrame()

        with self.assertLogs(level="WARNING") as log:
            upload_ke_sheet(df)

        self.assertTrue(any("Tidak terdapat data untuk diupload" in message for message in log.output))

if __name__ == "__main__":
    unittest.main()

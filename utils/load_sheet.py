import pandas as pd
import logging
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ganti dengan ID spreadsheet kamu
SPREADSHEET_ID = "1M5McHLszQp3lu0-tykrh36nP4QLfmgdEon41dOp42rM"
SHEET_NAME = "Sheet1"  # Tab aktif di Google Sheets

def upload_ke_sheet(df: pd.DataFrame):
    """
    Mengunggah DataFrame ke Google Sheets.
    """
    if df.empty:
        logger.warning("Tidak terdapat data untuk diupload")
        return

    try:
        creds = service_account.Credentials.from_service_account_file(
            "google-sheets-api.json",
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        values = [df.columns.tolist()] + df.values.tolist()

        request = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A1",
            valueInputOption="RAW",
            body={"values": values}
        )
        response = request.execute()

        logger.info(f"Data berhasil diupload ke tab '{SHEET_NAME}' di Google Sheets.")
        return response

    except Exception as e:
        logger.error(f"Terjadi kesalahan saat mengunggah ke Google Sheets: {e}")
        return None

# Alias agar kompatibel dengan unit test lama
load_to_google_sheets = upload_ke_sheet

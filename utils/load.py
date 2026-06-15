
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine

def save_to_csv(df):
    try:
        df.to_csv("products.csv", index=False)
        return True
    except Exception as e:
        print(f"Gagal menyimpan CSV: {e}")
        return False


def save_to_google_sheets(df):
  try:
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        "google-sheets-api.json",
        scopes=scope
    )

    client = gspread.authorize(creds)

    spreadsheet = client.open("etl-fashion-data")
    worksheet = spreadsheet.sheet1

    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    return True

  except Exception as e:
        print(f"Google Sheets load error: {e}")
        return False


def save_to_postgresql(df):
  try:

    SUPABASE_DB_URL = "postgresql+psycopg2://postgres.okdhdziensupdgpeymfk:QFPBdDG2e17sdngZ@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require"

    supabase_engine = create_engine(SUPABASE_DB_URL)

    df.to_sql("products", supabase_engine, if_exists="replace", index=False)
    return True
  except Exception as e:
        print(f"PostgreSQL load error: {e}")
        return False

  
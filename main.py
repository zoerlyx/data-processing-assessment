
# import fungsi pipeline
from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets, save_to_postgresql

def run_pipeline():
    # Extract
    print("Scraping...")
    df_raw = scrape_main()
    if df_raw is None or df_raw.empty:
        raise ValueError("scrape_main() mengembalikan data kosong!")
    print(f"Scraping selesai: {len(df_raw)} baris")

    # Transform
    print("Transform...")
    df_clean = transform_data(df_raw)
    print(f"Transform selesai: {df_clean.shape}")

    # Load
    print("Loading...")
    save_to_csv(df_clean)
    save_to_google_sheets(df_clean)
    save_to_postgresql(df_clean)
    print("Pipeline selesai!")

    return df_clean


df_result = run_pipeline()
df_result.head()

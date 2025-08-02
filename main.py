# main.py

from utils.extract import extract_data_from_api

if __name__ == "__main__":
    url = "https://fashion-studio.dicoding.dev/products"  # URL API yang benar
    df = extract_data_from_api(url)
    
    print(df.head())  # Tampilkan 5 data pertama untuk cek apakah berhasil

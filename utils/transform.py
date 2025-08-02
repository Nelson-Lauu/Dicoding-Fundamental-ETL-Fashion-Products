import pandas as pd

EXCHANGE_RATE = 16000

def transform_data(data):
    """
    Membersihkan dan mengubah format data

    Transformasi:
    - Mengonversi harga USD ke Rupiah
    - Ekstrak angka dari kolom rating
    - Ubah colors jadi int (jumlah warna)
    - Hapus data duplikat dan tidak valid
    """
    try:
        df = pd.DataFrame(data).copy()

        if df.empty:
            print("Data kosong setelah scraping")
            return df

        required_columns = {"Price", "Rating", "Colors", "Title"}
        if not required_columns.issubset(df.columns):
            missing_cols = required_columns - set(df.columns)
            print(f"Terdapat kolom yang tidak ditemukan: {missing_cols}")

        # Ubah Price jadi Rupiah
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce") * EXCHANGE_RATE

        # Ekstrak angka dari Rating
        df["Rating"] = df["Rating"].astype(str).str.extract(r"([\d.]+)").astype(float)

        # Ubah Colors ke integer (jumlah warna)
        df["Colors"] = pd.to_numeric(df["Colors"], errors="coerce").fillna(0).astype(int)

        # Hapus data duplikat dan null
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)

        # Filter produk dengan judul "Produk Tidak Dikenal"
        df = df[df["Title"] != "Unknown Product"]

        print("Proses transformasi selesai.")
        return df

    except Exception as e:
        print(f"Error saat proses transformasi: {e}")
        return pd.DataFrame()

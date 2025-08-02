import pandas as pd

def simpan_ke_csv(dataframe: pd.DataFrame, nama_file="products.csv"):
    """
    Menyimpan DataFrame ke file CSV.

    Parameters:
    dataframe (pd.DataFrame): Data yang akan disimpan.
    nama_file (str): Nama file output (default: "products.csv")

    Returns:
    None
    """
    if dataframe.empty:
        print("Tidak terdapat data untuk disimpan.")
        return

    try:
        dataframe.to_csv(nama_file, index=False)
        print(f"Data berhasil disimpan di {nama_file}")
    except Exception as e:
        print(f"Error saat menyimpan data ke CSV: {e}")
        raise

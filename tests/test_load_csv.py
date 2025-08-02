import sys
import os

# ✅ Tambahkan folder root ke path agar 'utils' bisa dikenali
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
import os
import tempfile
from utils.load_data.load_csv import simpan_ke_csv

class TestSimpanCSV(unittest.TestCase):

    def setUp(self):
        # Buat file sementara untuk menyimpan data saat test
        self.tempfile = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        self.temp_path = self.tempfile.name
        self.tempfile.close()

    def tearDown(self):
        # Hapus file CSV setelah pengujian
        if os.path.isfile(self.temp_path):
            os.remove(self.temp_path)

    def test_simpan_csv_berhasil(self):
        # Cek apakah data berhasil ditulis ke file CSV
        sample_data = {
            "Title": ["Contoh Produk"],
            "Price": [150000],
            "Rating": [4.7],
            "Colors": [2],
            "Size": ["L"],
            "Gender": ["Female"]
        }
        df = pd.DataFrame(sample_data)

        simpan_ke_csv(df, self.temp_path)

        self.assertTrue(os.path.exists(self.temp_path))

        hasil_baca = pd.read_csv(self.temp_path)
        pd.testing.assert_frame_equal(df, hasil_baca, check_dtype=False)

    def test_simpan_csv_gagal(self):
        # Pastikan error ditangani saat lokasi file tidak valid
        sample_data = {
            "Title": ["Produk Error"],
            "Price": [175000],
            "Rating": [4.3],
            "Colors": [1],
            "Size": ["S"],
            "Gender": ["Unisex"]
        }
        df = pd.DataFrame(sample_data)

        # Lokasi yang tidak valid (umumnya gagal di semua OS)
        path_salah = "/lokasi_tidak_ada/fileku.csv"

        with self.assertRaises(Exception):
            simpan_ke_csv(df, path_salah)

if __name__ == "__main__":
    unittest.main()

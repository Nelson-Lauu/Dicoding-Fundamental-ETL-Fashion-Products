# import packages yang akan digunakan
import time
import requests
import datetime
from bs4 import BeautifulSoup

# headers (sc: dicoding)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

BASE_URL = "https://fashion-studio.dicoding.dev/"
max_halaman = 50
max_data = 1000

# fungsi untuk scraping satu halaman
def scrape_page(url: str) -> list:
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Terjadi kesalahan ketika request ke {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for produk in soup.find_all("div", class_="collection-card"):
        judul_elem = produk.find("h3", class_="product-title")
        judul = judul_elem.text.strip() if judul_elem else "Unknown Product"

        harga_elem = produk.find("span", class_="price")
        harga = harga_elem.text.strip().replace("$", "") if harga_elem else "N/A"

        rating_elem = produk.find("p", string=lambda teks: teks and "Rating" in teks)
        rating = rating_elem.text.replace("Rating:", "").replace("⭐", "").strip() if rating_elem else "Invalid"

        warna_elem = produk.find("p", string=lambda teks: teks and "Colors" in teks)
        warna = warna_elem.text.replace("Colors:", "").strip().split()[0] if warna_elem else "N/A"

        ukuran_elem = produk.find("p", string=lambda teks: teks and "Size" in teks)
        ukuran = ukuran_elem.text.replace("Size:", "").strip() if ukuran_elem else "N/A"

        gender_elem = produk.find("p", string=lambda teks: teks and "Gender" in teks)
        gender = gender_elem.text.replace("Gender:", "").strip() if gender_elem else "N/A"

        waktu_scraping = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        products.append({
            "Title": judul,
            "Price": harga,
            "Rating": rating,
            "Colors": warna,
            "Size": ukuran,
            "Gender": gender,
            "Timestamp": waktu_scraping
        })

    return products

# fungsi untuk scraping semua halaman
def scrape_main():
    all_products = []
    for halaman in range(1, max_halaman + 1):
        url = BASE_URL if halaman == 1 else f"{BASE_URL}page{halaman}"
        print(f"Scraping URL: {url}")
        data_halaman = scrape_page(url)
        print(f"Jumlah produk ditemukan: {len(data_halaman)}")

        all_products.extend(data_halaman)
        if len(all_products) >= max_data:
            break
        time.sleep(1)

    print(f"\nTotal data scraping: {len(all_products)}")
    return all_products

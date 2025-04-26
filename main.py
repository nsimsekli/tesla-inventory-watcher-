import requests
import time
import json

# Tesla API URL - Türkiye Model Y yeni araçlar
TESLA_API_URL = "https://www.tesla.com/inventory/api/v1/inventory-results?query=%7B%22options%22%3A%7B%7D%2C%22query%22%3A%7B%22model%22%3A%22my%22%2C%22condition%22%3A%22new%22%2C%22arrangeby%22%3A%22Relevance%22%2C%22zip%22%3A%2203434%22%2C%22range%22%3A0%2C%22region%22%3A%22EU%22%2C%22language%22%3A%22tr%22%2C%22super_region%22%3A%22emea%22%7D%2C%22offset%22%3A0%2C%22count%22%3A50%7D"

CHECK_INTERVAL = 60  # Saniye cinsinden aralık (isteğe göre ayarlanabilir)

def fetch_inventory():
    response = requests.get(TESLA_API_URL)
    data = response.json()
    vehicles = data.get('results', [])
    return [vehicle['VIN'] for vehicle in vehicles]  # Sadece VIN (araç kimlik) numaralarını çekiyoruz

def main():
    previous_vins = set()

    while True:
        try:
            current_vins = set(fetch_inventory())
            new_vins = current_vins - previous_vins

            if new_vins:
                print("YENİ ARAÇ BULUNDU!")
                for vin in new_vins:
                    print(f"Yeni Araç VIN: {vin}")

            previous_vins = current_vins
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print("Hata oluştu:", e)
            time.sleep(10)  # Hata oluşursa kısa bir bekleme ile devam et

if __name__ == "__main__":
    main()

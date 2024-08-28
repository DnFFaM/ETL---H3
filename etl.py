import requests
import time
import csv
import os

# Global variabel til at holde data
data = []

# Extract-funktion
def extract():
    global data
    url = "https://api.energidataservice.dk/dataset/Elspotprices?offset=0&sort=HourUTC%20DESC"  # Tilpas URL'en til dit behov
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        data = json_data.get("records", [])
    else:
        print("Failed to fetch data. Status code:", response.status_code)

# Transform-funktion
def transform():
    global data
    # I dette tilfælde er det kun nødvendigt at ændre formatet på nogle felter
    for record in data:
        record['HourUTC'] = record['HourUTC'].replace('T', ' ').replace('Z', '')
        record['SpotPriceEUR'] = float(record['SpotPriceEUR'])

# Load-funktion
def load():
    global data
    file_exists = os.path.isfile('elspotprices.csv')
    with open('elspotprices.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["HourUTC", "SpotPriceEUR", "PriceArea"])
        for record in data:
            writer.writerow([record['HourUTC'], record['SpotPriceEUR'], record['PriceArea']])
    print("Data gemt til elspotprices.csv")

# Main-funktion
def main():
    while True:
        extract()
        transform()
        load()
        time.sleep(60)  # Pauser i 1 minute før næste kørsel

if __name__ == "__main__":
    main()

# skracanie kolumny z csv
import csv

def skroc_kolumne(plik_wejsciowy, plik_wyjsciowy):
    with open(plik_wejsciowy, 'r') as file:
        csv_reader = csv.reader(file, delimiter='|')
        rows = list(csv_reader)

        for row in rows:
            if len(row) >= 2:
                if len(row[1]) > 100:
                    row[1] = row[1][:100]  # Skracamy drugą kolumnę do 100 znaków

    with open(plik_wyjsciowy, 'w', newline='') as file:
        csv_writer = csv.writer(file, delimiter='|')
        csv_writer.writerows(rows)

plik_wejsciowy = '/home/marcel/Documents/scrapper/projekt-be/scraper/csv_to_shorten/products.csv'  # Zmień nazwę pliku wejściowego
plik_wyjsciowy = '/home/marcel/Documents/scrapper/projekt-be/scraper/csv_to_shorten/products2.csv'  # Zmień nazwę pliku wyjściowego

skroc_kolumne(plik_wejsciowy, plik_wyjsciowy)
import csv

if __name__ == "__main__":
    csv_path = r"d:\!SAVE\SCV777\3.csv"
    with open(csv_path, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            print(" ".join(row))

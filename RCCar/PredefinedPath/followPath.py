import csv

with open('data/state_data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)

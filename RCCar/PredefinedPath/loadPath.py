import csv

def loadPath(file_name='test_data.csv'):
    with open(file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            print(row)
            print(row[0])
            print(row[0],row[1],row[2],)

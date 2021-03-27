import csv
import psycopg2
import math
import unidecode
import os , shutil
import time
import bonobo
import requests
import sys


DATA_STORE = []
try:
    DATA_SOURCE = str(sys.argv[1])
except:
    DATA_SOURCE = "source_humidity.csv"

def csv_data(file_path):
    row_count = 0
    city_data = []
    year_data = []
    file_data = []
    with open('data/'+file_path, encoding='utf-8') as f:
        data = csv.reader(f)
        row_count = sum(1 for row in data)
        #print(row_count)
    with open('data/'+file_path, encoding='utf-8') as a:
        data = csv.reader(a)
        i = 0
        row_split = []
        for row in data:      
            if i == 2:
                row_split = row[0].split(';')
                for j in range(len(row_split)):
                    year_data.append(row_split[j][1:5]) if row_split[j] != '" "' else year_data.append('') 
            if i >= 4 and i < row_count:
                row_split = row[0].split(';')
                os.system('clear')
                # print(str(i-3)+'---Extracted Line')
                #print(row) 
                city_data.append(row_split[0])     
                file_data.append(row_split[1:len(row[0].split(';'))]) 
            i+=1

        # data_transfer = []
        # file_data_transfer = []
        # for data in file_data:
        #     for numb in data:
        #         data_transfer.append(str(round(float(numb)))[:2])
        #     file_data_transfer.append(data_transfer)
        #     data_transfer = []
        # print(file_data_transfer)   

        return city_data, year_data[1:], file_data


def transfer_to_structured_data(fileName, *args):
    storeData = []
    for arg in args:
        storeData.append(arg)
    with open('{}'.format(fileName), 'w', newline='') as csv_file:
        fileName = fileName[:-4]
        writer = csv.writer(csv_file)
        writer.writerow(["city", "year", fileName[7:]])
        city = storeData[0]
        year = storeData[1]
        data = storeData[2]
        for i in range(len(city)):
            dataIndex = data[i]
            for j in range(len(dataIndex)):
                writer.writerow([city[i], year[j], dataIndex[j]])
    os.system('python3 move_files.py')


# def get_structured_data(fileName):
#     city_data, year_data, file_data = csv_data("{}".format(fileName))
#     transfer_to_structured_data("{}".format(fileName),city_data, year_data, file_data)



def extract_data_from_csv():
    city_data, year_data, file_data = csv_data("{}".format(DATA_SOURCE))
    yield city_data
    yield year_data
    yield file_data


def transform_data(args: list):
    DATA_STORE.append(args)
    yield DATA_STORE
    


def load_into_new_csv_file(args: list):
    city_data, year_data, file_data = DATA_STORE
    transfer_to_structured_data("{}".format(DATA_SOURCE), city_data, year_data, file_data)

    



def main():
    

    graph = bonobo.Graph(
        extract_data_from_csv,
        transform_data,
        load_into_new_csv_file
    )
    bonobo.run(graph)
    


if __name__ == "__main__":
    main()
    


    
    


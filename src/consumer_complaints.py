import sys
import os
import csv

def read_data(filename):
    '''
    read data from the input file
    '''
    fp = open(filename, newline="")
    fp.readline()
    reader = csv.reader(fp)
    data = []
    for row in reader:
        date = row[0]
        product = row[1].lower()
        company = row[7].lower()
        tokens = date.split("-")
        year = tokens[0]
        year = int(year)
        data.append([year, product, company])
    return data

def get_years(data):
    '''
    get all the unique years
    '''
    years = []
    for item in data:
        if item[0] not in years:
            years.append(item[0])
    return years

def get_unique_products(data, year):
    '''
    get all the unique products by the year
    '''
    products = []
    for item in data:
        if item[0] == year:
            if item[1] not in products:
                products.append(item[1])
    return products


def get_complaints_number(data, year, product):
    '''
    get the total number of complaints for the product
    '''
    count = 0
    for item in data:
        if item[0] == year and item[1] == product:
            count += 1
    return count

def get_company_count(data, year, product):
    '''
    get the complaints number for each company
    '''
    result = {}
    for item in data:
        if item[0] == year and item[1] == product:
            if item[2] not in result:
                result[item[2]] = 1
            else:
                result[item[2]] += 1
    return result




def main():
    args = sys.argv
    if len(args) !=3:
        print("usage: python consumer_complaints.py input_filepath output_filepath")
        return 
    infile = args[1]
    outfile = args[2]
    if not os.path.isfile(infile):
        print("input file not exist")
        return
    # infile = "../insight_testsuite/test_1/input/complaints.csv"
    # outfile = "./report.csv"
    data = read_data(infile)
    years = get_years(data)
    years.sort()
    report = []
    for year in years:
        products = get_unique_products(data, year)
        products.sort()
        for product in products:
            total = get_complaints_number(data, year, product)
            freqs = get_company_count(data, year, product)
            freqs = list(freqs.items())
            freqs.sort(key=lambda x:x[1], reverse=True)
            percent = round(100*freqs[0][1]/total)
            report.append([product, year, total, len(freqs), percent])
    report.sort(key=lambda x:x[1])
    report.sort(key=lambda x:x[0])
    with open(outfile, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        for row in report:
            writer.writerow(row)



if __name__ == "__main__":
    main()
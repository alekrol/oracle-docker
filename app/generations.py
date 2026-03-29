import csv
from models import SwimmingClass, SwimmingPool, SwimmingSchool, Instructor, CoursePayment, Customer, Multisport

def generate_swimming_school_data(n=50):
    names = open('example-data/swimming-school-names.txt', 'r').read().splitlines()
    descriptions = [d['description'] for d in csv.DictReader()]

    with open('example-data/swim-descriptions.csv', 'r') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            descriptions.append(row['description'])
    
    rows = min(len(names), len(descriptions))

    with open('data-for-db-import/swimming-schools-descriptions.csv', 'rw') as f:
        writer = csv.writer()
        writer.writerow(['id', 'name', 'description'])

        for row in range(rows):
            writer.writerow([row])

def h():
    with open('example-data/swimming-school-names.csv', 'w') as write_file:
        with open('example-data/swimming-school-names.txt', 'r') as read_file:
            names = read_file.read().splitlines()
            writer = csv.writer()
            writer.writerow(['id', 'name'])
            writer.writerows(names)

if __name__ == '__main__':
    h()
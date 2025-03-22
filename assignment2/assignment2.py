import csv
import traceback
def read_employees():
    employees_dict = dict()
    employees_row = list()
    
    try:
        with open('../csv/employees.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            employees_dict['fields'] = header
            for row in reader:
                employees_row.append(row)
            employees_dict['rows'] = employees_row
            return employees_dict
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"An exception occurred. Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")

employees = read_employees()
# print(employees)

# Task 3
def column_index(header: str):
    return employees['fields'].index(header)

employee_id_column = column_index('employee_id')
# print(f'{employee_id_column}')
# Task 4
def first_name(row):
    idx_of_first_name = column_index('first_name')
    return employees['rows'][row][idx_of_first_name]
# print(first_name(1))

# Task 5
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    matches = list(filter(employee_match, employees['rows']))
    return matches

# print(employee_find(2))

# Task 6
def employee_find_2(employee_id):
    matches = list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"]))
    return matches

# Task 7
def sort_by_last_name():
    employees['rows'].sort(key=lambda row: row[column_index('last_name')])
    return employees['rows']
# print(sort_by_last_name())

# Task 8
def employee_dict(row):
    fields_exclude_employee_id = employees["fields"][1:]
    return dict(zip(fields_exclude_employee_id, row[1:]))
# print(employee_dict(employees['rows'][0]))

#Task 9
def all_employees_dict():
    res = {}
    for row in employees["rows"]:
        res[row[0]] = employee_dict(row)    
    return res
# print(all_employees_dict())

# Task 10

import os
def get_this_value():
    return os.getenv("THISVALUE")

# print(get_this_value())

# Task 11
import custom_module
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)
    print(custom_module.secret)
# print(set_that_secret("this is a new secret"))

# Task 12

filenames = ['../csv/minutes1.csv', '../csv/minutes2.csv']
minutes1 = None
minutes2 = None

def read_csv_file(filename):
    result = {}
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            result['fields'] = header
            result['rows'] = []
            for row in reader:
                result['rows'].append(tuple(row))
            return result
            
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"An exception occurred. Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
def read_minutes():
    global minutes1, minutes2
    minutes1 = read_csv_file(filenames[0])
    minutes2 = read_csv_file(filenames[1])
    return minutes1, minutes2

minutes1, minutes2 = read_minutes()
# print(minutes2, minutes2)

minutes_set = None

# Task 13
def create_minutes_set():
    minutes1_set = set(minutes1['rows'])
    minutes2_set = set(minutes2['rows'])
    combined_both_sets = minutes1_set.union(minutes2_set)
    return combined_both_sets
    
minutes_set = create_minutes_set()

# Task 14
from datetime import datetime

def create_minutes_list():
    return list(map(lambda row: (row[0], datetime.strptime(row[1], "%B %d, %Y")), minutes_set))

minutes_list = create_minutes_list()
# print(minutes_list)

# Task 15
def write_sorted_list():
    sorted_by_datetime = sorted(minutes_list, key=lambda row: row[1])
    result_list = list(map(lambda row: (row[0], datetime.strftime(row[1], "%B %d, %Y")), sorted_by_datetime))
    try:
        with open('./minutes.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(minutes1['fields'])
            for row in result_list:
                 writer.writerow(row)
            
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"An exception occurred. Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
    return result_list
write_sorted_list()
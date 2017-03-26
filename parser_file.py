### Created by Thibault Timmerman, Subhadeep Roy, Nishtha GARG, Joeldeep Kaur
###     On 2/26/2017

import csv

# Parsing a line to remove '/' and '|' and get the data which is converted in float to be used in the calculation tasks
def line_parser(line):
    # Counting variables
    j = 0  # Local variable to count the number of /

    # Data variables
    temp_string = ''
    point = [0, 0, 0]
    points_matrix = []

    # Parsing the line
    for char in line:
        if char != '|' and char != '':
            if char != '/':
                temp_string += char
            elif char == '/':
                point[j] = float(temp_string)
                temp_string = ''  # Reinitialization of buffer
                j += 1
        elif char == '|':
            points_matrix.append(point)
            point = [0, 0, 0]  # Reinitialization of point table
            j = 0  # Reinitialization of counting variable
            temp_string = ''  # Reinitialization of buffer

    # Append the last point to the matrix after parsing, otherwise it is not appended
    points_matrix.append(point)

    return points_matrix


# Parsing a line to remove '/' and '|' and get the data which is converted in float to be used in the calculation tasks (for two data)
def slope_parser(line):
    # Counting variables
    j = 0  # Local variable to count the number of /

    # Data variables
    temp_string = ''
    point = [0, 0]
    points_matrix = []

    # Parsing the line
    for char in line:
        if char != '|' and char != '':
            if char != '/':
                if char != '-':
                    temp_string += char
                    point[j] = float(temp_string)
            elif char == '/':
                #point[j] = float(temp_string)
                temp_string = ''  # Reinitialization of buffer
                j += 1
        elif char == '|':
            point[j] = float(temp_string)
            points_matrix.append(point)
            point = [0, 0]  # Reinitialization of point table
            j = 0  # Reinitialization of counting variable
            temp_string = ''  # Reinitialization of buffer

    # Append the last point to the matrix after parsing, otherwise it is not appended
    points_matrix.append(point)

    return points_matrix


def put_in_list(f):
    q = []
    file = open(f, "rb")
    reader = csv.reader(file)
    for row in reader:
        q.append(row)
    file.close()
    return q
    
def create_outputFile(result, filename):
    f = open(filename, "wb")    
    outputFile = csv.writer(f)
    for row in result:
        outputFile.writerow(row)
    f.close()  

    return 0
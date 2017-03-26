### Created by Thibault Timmerman, Subhadeep Roy, Nishtha GARG, Joeldeep Kaur
###     On 2/26/2017

import time
import math
import math_functions as mfunc
import parser_file as pars
from multiprocessing import Process
import sys


# This function finds the shortest distance from a point to a line (list of possible links points)
def find_shortest_distance(matches_list, point):
    shortest_linkdistance = 1000
    ref_node_dist = 0
    ref_link_id = 0
    for list in matches_list:
        i = 0
        while i < len(list[18]) - 1:
            pointA = mfunc.convert_latLong(list[18][i][0], list[18][i][1])
            pointB = mfunc.convert_latLong(list[18][i + 1][0], list[18][i + 1][1])
            link = mfunc.vector3d(pointA, pointB)
            distance = mfunc.calc_distance_point_line(link, point, pointA)
            if distance < shortest_linkdistance:
                shortest_linkdistance = distance
                ref_link_id = list[0]
                ref_node_dist = list[17]
            i += 1
    return shortest_linkdistance, ref_link_id, ref_node_dist


def determine_direction(list, link_id, distance):
    direction = ''
    if not list:
        pass
    else:
        if list[-1][8] == link_id:
            if distance >= float(list[-1][10])*10:
                direction = 'F'
            else:
                print 'try'
                direction = 'T'
            # Extend the deduction to the first point of the list if possible.
            # We check if the field is empty two points before the point currently analyzed.
            # If it is the case, we complete the field we F or T according to the current point.
            if len(list) >= 2:
                if list[-2][9] == '' and list[-2][8] == link_id:
                    list[-2][9] = direction
    return direction


def process_row(row, result_list, list):
    # Temporary variable used to store the data
    possible_matches = []
    temp = []
    # Convert the probe point latitude and longitude into coordinates
    probePoint = mfunc.convert_latLong(float(row[3]), float(row[4]))

    for line in list:
        # Create the matrix with the different point of the link (Reference point first, shape point and no reference points)
        points_table = pars.line_parser(line[14])
        link_length = float(line[3])  # Convert link length into float for future use

        # Compute the distance between the probe point and the reference point
        distance = mfunc.calc_distance_points(points_table[0][0], points_table[0][1], float(row[3]), float(row[4]))

        if mfunc.compare_distance(distance, link_length):
            # We calculate the orthogonal distance
            temp = line[:]
            temp.append(distance)  # Append in 18th position, get it calling line[17]
            temp.append(points_table)  # Append in 19th position, get it calling line[18]
            possible_matches.append(temp)

    # Test and find what is the best match
    linkdistance, ref_link_id, ref_node_dist = find_shortest_distance(possible_matches, probePoint)

    # Compute the direction of the point: 'From' or 'To' Ref point.
    direction = determine_direction(result_list, ref_link_id, ref_node_dist)

    # Create the row for output file
    row.append(ref_link_id)
    row.append(direction)
    row.append(ref_node_dist / 10)
    row.append(linkdistance / 10)

    # Add the row to the result list
    result_list.append(row)

    possible_matches[:] = []
    temp[:] = []

    # Print progress bar at every 5 percent    
    percent = int(len(result_list) * 100 / TotalPoints)

    if percent % 5 == 0:
          sys.stdout.write("%s%%..." % percent)
          sys.stdout.flush()

    return 0


def job(point_list, q, str):
    outputfile = "./TempMatchedPoints" + str +  ".csv"
    result = []

    for row in point_list:
        process_row(row, result, q)

    pars.create_outputFile(result, outputfile)

    return 0

def main():
    LinksFile = "./Partition6467LinkData.csv"
    ProbePointsFile = "./Partition6467ProbePoints.csv"
    outputfile = "./Partition6467MatchedPoints.csv"

    # Open all file needed
    start_time = time.time()

    # Charge data into memory
    q = pars.put_in_list(LinksFile)
    points = pars.put_in_list(ProbePointsFile)
    print('File loading complete...')
    #points = points[0:20]      # points sliced for testing only

    global TotalPoints 
    TotalPoints = len(points)

    # Variable used to count the lines read in linkData
    SetPartPoints = 20
    threads = [Process(target=job,
                       args=(points[0:int(math.floor(len(points)/SetPartPoints))], q, '0')),
               Process(target=job,
                       args=(points[int(math.floor(len(points)/SetPartPoints)) + 1:2 * int(math.floor(len(points)/SetPartPoints))], q, '1')),
               Process(target=job,
                       args=(points[int(math.floor(2* len(points)/SetPartPoints)) + 1:3 * int(math.floor(len(points) / SetPartPoints))], q,'2')),
               Process(target=job,
                       args=(points[int(math.floor(3 * len(points) / SetPartPoints)) + 1:4 * int(math.floor(len(points) / SetPartPoints))], q, '3')),
               Process(target=job,
                       args=(points[int(math.floor(4 * len(points) / SetPartPoints)) + 1:5 * int(math.floor(len(points) / SetPartPoints))], q, '4')),
               Process(target=job,
                       args=(points[int(math.floor(5 * len(points) / SetPartPoints)) + 1:6 * int(math.floor(len(points) / SetPartPoints))], q, '5')),
               Process(target=job,
                       args=(points[int(math.floor(6 * len(points) / SetPartPoints)) + 1:7 * int(math.floor(len(points) / SetPartPoints))], q, '6')),
               Process(target=job,
                       args=(points[int(math.floor(7 * len(points) / SetPartPoints)) + 1:8 * int(math.floor(len(points) / SetPartPoints))], q, '7')),
               Process(target=job,
                       args=(points[int(math.floor(8 * len(points) / SetPartPoints)) + 1:9 * int(math.floor(len(points) / SetPartPoints))], q, '8')),
               Process(target=job,
                       args=(points[int(math.floor(9 * len(points) / SetPartPoints)) + 1:10 * int(math.floor(len(points) / SetPartPoints))], q, '9')),
               Process(target=job,
                       args=(points[int(math.floor(10 * len(points) / SetPartPoints)) + 1:11 * int(math.floor(len(points) / SetPartPoints))], q, '10')),
               Process(target=job,
                       args=(points[int(math.floor(11 * len(points) / SetPartPoints)) + 1:12 * int(math.floor(len(points) / SetPartPoints))], q, '11')),
               Process(target=job,
                       args=(points[int(math.floor(12 * len(points) / SetPartPoints)) + 1:13 * int(math.floor(len(points) / SetPartPoints))], q, '12')),
               Process(target=job,
                       args=(points[int(math.floor(13 * len(points) / SetPartPoints)) + 1:14 * int(math.floor(len(points) / SetPartPoints))], q, '13')),
               Process(target=job,
                       args=(points[int(math.floor(14 * len(points) / SetPartPoints)) + 1:15 * int(math.floor(len(points) / SetPartPoints))], q, '14')),
               Process(target=job,
                       args=(points[int(math.floor(15 * len(points) / SetPartPoints)) + 1:16 * int(math.floor(len(points) / SetPartPoints))], q, '15')),
               Process(target=job,
                       args=(points[int(math.floor(16 * len(points) / SetPartPoints)) + 1:17 * int(math.floor(len(points) / SetPartPoints))], q, '16')),
               Process(target=job,
                       args=(points[int(math.floor(17 * len(points) / SetPartPoints)) + 1:18 * int(math.floor(len(points) / SetPartPoints))], q, '17')),
               Process(target=job,
                       args=(points[int(math.floor(18 * len(points) / SetPartPoints)) + 1:19 * int(math.floor(len(points) / SetPartPoints))], q, '1')),
               Process(target=job,
                       args=(points[int(math.floor(19 * len(points) / SetPartPoints)) + 1:len(points)], q, '1'))]
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("\n--- %s seconds ---" % (time.time() - start_time))

    return 0

# Start the program.
main()

### Created by Thibault Timmerman, Subhadeep Roy, Nishtha GARG, Joeldeep Kaur
###     On 2/26/2017

import math
import parser_file as pars
import copy
import math_functions as mfunc


distance_position_inList = 10


def compare_list(listA, listB):
    if float(listA[distance_position_inList]) < float(listB[distance_position_inList]):
        return -1
    elif float(listA[distance_position_inList]) > float(listB[distance_position_inList]):
        return 1
    else:
        return 0


# Derive slope for each link using probe points
def derive_slope(list, linkList):
    # Temporary list with original data
    temp_list = copy.deepcopy(list)
    comparison_table = []
    outputfile = "./SlopeComparison.csv"
    header = 'linkPVID, mean_surveyed, mean_slope, abs_err, rel_err'

    for row_number, row in enumerate(list):
        pointsOnLink = []
        # Avoid calculating the slope for the same set of probe points twice
        if float(row[8]) != -1:
            pointsOnLink.append(temp_list[row_number])
            # Create a table with the set of probe points on the same link
            for line_number, line in enumerate(list[row_number+1:]):
                if line[8] == row[8]:
                    pointsOnLink.append(temp_list[line_number+row_number+1])
                    line[8] = -1
            row[8] = -1

            # Sort the list from the smallest distance to the longest from the ref point of the link
            pointsOnLink.sort(cmp=compare_list)
            #print len(pointsOnLink), pointsOnLink

            # Compute slope angle and compare with survey in linksFile
            if len(pointsOnLink) > 1:
                mean_slope = 0
                sum_slope = 0
                for l_num, l in enumerate(pointsOnLink[:len(pointsOnLink)-1]):
                    # Calculate the slope
                    slope_rad = mfunc.compute_slope(float(l[5]), float(pointsOnLink[l_num+1][5]), float(l[10])*10, float(pointsOnLink[l_num+1][10])*10)
                    #print float(l[5]), float(pointsOnLink[l_num+1][5]), float(l[10])*10, float(pointsOnLink[l_num+1][10])*10
                    slope_deg = math.degrees(slope_rad)
                    sum_slope += slope_deg

                mean_slope = sum_slope / (l_num + 1)

                # Calculate the mean slope for the survey links
                for li in linkList:
                    # Check if the link is the link which was matched to the probe points.
                    if l[8] == li[0]:
                        #print li[0], l[8]
                        mean_surveyed = 0
                        sum_surveyed = 0
                        # parse the line of slope points
                        point_table = pars.slope_parser(li[16])
                        #print point_table
                        if point_table:
                            for data_num, data in enumerate(point_table[:len(point_table)-1]):
                                sum_surveyed += data[1]

                            mean_surveyed = sum_surveyed / (data_num + 1)

                        abs_err, rel_err = mfunc.compare_slope(mean_slope, mean_surveyed)

                        comparison_table.append([li[0], mean_surveyed, mean_slope, abs_err, rel_err])

            # Initialization of variables.
            pointsOnLink[:] = []

    pars.create_outputFile(comparison_table, outputfile)


def main():
    # Variables initialization
    inputFile = "./Partition6467MatchedPoints.csv"
    linksFile = "./Partition6467LinkData.csv"
    points_list = pars.put_in_list(inputFile)
    links_list = pars.put_in_list(linksFile)
    print('File loading complete...')
    derive_slope(points_list, links_list)

    return 0

# Start deriving slope 
main()

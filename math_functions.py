### Created by Thibault Timmerman, Subhadeep Roy, Nishtha GARG, Joeldeep Kaur
###     On 2/26/2017

import math

earth_radius = 6367445  # Medium Earth radius in meters


# Used to compute the vector
def convert_latLong(latitude, longitude):
    long = math.radians(longitude)
    lat = math.radians(latitude)
    x = earth_radius * math.cos(long) * math.cos(lat)
    y = earth_radius * math.sin(long) * math.cos(lat)
    z = earth_radius * math.sin(lat)
    return [x, y, z]


# Used to calculate the distance betzeen a line and a point
def vector3d(pointA, pointB):
    coordinates = [pointB[0] - pointA[0], pointB[1] - pointA[1], pointB[2] - pointA[2]]  # Make sure A is the reference point
    return coordinates


def vector_norm(vect):
    norm = math.sqrt(vect[0]**2 + vect[1]**2 + vect[2]**2)
    return norm


def vector_multiplication(vect1, vect2):
    x = vect1[1] * vect2[2] - vect2[1] * vect1[2]
    y = vect1[2] * vect2[0] - vect2[2] * vect1[0]
    z = vect1[0] * vect2[1] - vect2[0] * vect1[1]
    return [x, y, z]


# Compute the distance between a point and a 3d vector (vector director of the link, probe point coordinates, ref point coordinates).
def calc_distance_point_line(dir_vector, point, refpoint):
    vect = vector3d(refpoint, point)  # Compute the vector between reference point and probe point
    multiply = vector_multiplication(dir_vector, vect)
    dist = vector_norm(multiply) / vector_norm(vect)

    return dist


# Distance with latitude and longitude, taking into account that Earth is not flat (lat, long pt A / lat long pt B).
def calc_distance_points(lA, LA, lB, LB):
    latA = math.radians(lA)
    latB = math.radians(lB)
    longA = math.radians(LA)
    longB = math.radians(LB)
    distance = earth_radius * math.acos(math.sin(latA) * math.sin(latB) + math.cos(latA) * math.cos(latB) * math.cos(longA - longB))

    return distance


# Compare the distance between two points
def compare_distance(dist1, dist2):
    if dist1 <= dist2:
        return True
    else:
        return False


# Calculate the slope on probe points (Altitude pt A, altitude pt B, distance from ref point pt A, distance from ref point pt B)
def compute_slope(alt_ptA, alt_ptB, distA, distB):
    delta_altitude = alt_ptB - alt_ptA
    delta_distance = distB - distA
    # The angle can be calculated using
    tan_angle = delta_altitude / delta_distance
    angle = math.atan(tan_angle)
    return angle

# Compare two slopes and return the absolute error and relative error.
def compare_slope(alt1, alt2):
    absolute_error = math.fabs(alt2 - alt1)
    if alt2 != 0:
        relative_error = math.fabs(absolute_error) / math.fabs(alt2)
    else:
        relative_error = 'undefined'
    return absolute_error, relative_error

# print vector_multiplication([2, 3, 4], [7, 4, 9])  # TODO Remove for release, function is working returns a correct result
# print vector_norm([1, 2, 4])  # TODO Remove for release, function is working returns a correct result
# pointA = convert_latLong(51.4965800, 9.3862299)  # TODO Remove for release, function is working returns a correct result
# pointB = convert_latLong(51.4994700, 9.3848799)  # TODO Remove for release, function is working returns a correct result
# ab = vector3d(pointA, pointB)  # TODO Remove for release, function is working returns a correct result
# print vector_norm(ab)  # TODO Remove for release, function is working returns a correct result
# pointC = convert_latLong(51.4966822229326,9.38615726307034)
# print calc_distance_point_line(ab, pointC, pointA)  # TODO Check if it works correctly, I think it does but I need to double check

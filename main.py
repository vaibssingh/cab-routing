# NOTE: Optimization should be on the basis of the total distance covered by ALL the cabs i.e find the optimal SET of cab routes where the total distance is minimum

# read coordinates from csv file of user, cabs and destination
# store the values into three variables as x,y coordinates in three variables
# using k-means clusterization, create groups of commuters
# for each group, calculate distance of each cab
# also add the distance to destination from the current location of the group to the previously calulcated distance <array of distances>
# from the above distances, find the minimum distance

import math
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans2, whiten
from geopy.distance import geodesic


def readFile():
    """This function reads the file and returns the coordinates in three different arrays for passengers, cabs and destination"""

    with open("input.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        # faltten the rows into one array containing arrays of coordinates (will give array of arrays)
        array_of_all_elements = []
        for line in csvreader:
            array_of_all_elements.append(line)

        # get the number of passengers from the first element of array which is also the first element of the input file
        number_of_passengers = array_of_all_elements[0][0]

        # based on number_of_passengers, access the main array and get coordinates till that element
        # skipping the 1st elm as that's the numbers of cars and people, also, array access by elements is NOT inclusive of the end index
        passenger_coordinates = array_of_all_elements[1:int(
            number_of_passengers) + 1]

        # similar to above, get list of cab coordinates
        # since the end index is NOT included, we only need to do '-1' which will still be the index of destination coordinates, instead of doing '-2'
        cab_coordinates = array_of_all_elements[int(
            number_of_passengers) + 1: (len(array_of_all_elements) - 1)]

        # get the last elm of array to get the destination coordinate
        destination_coordinate = array_of_all_elements[(
            len(array_of_all_elements) - 1)]

        return (passenger_coordinates, cab_coordinates, destination_coordinate)


# read the csv file and get the coordinates
passenger_coordinates, cab_coordinates, destination_coordinate = readFile()

# converting the list to have float element values instead of string (so that kmeans can be done and plotted)
passenger_coordinates_np = np.array(passenger_coordinates).astype(np.float)

# making array type uniform <numpy.ndarray>
cab_coordinates_np = np.array(cab_coordinates).astype(np.float)
destination_coordinate_np = np.array(destination_coordinate).astype(np.float)

# applying the kmeans2 cluterisation method (creating three clusters here based upon distribution as seen in graph)
passenger_group_coordinates, y = kmeans2(passenger_coordinates_np, 3, iter=10)

def find_destination_distance(passenger_coordinates_np, destination_coordinate_np):
    """Function to calculate distance of destination from current location of group"""
    for pass_coord in passenger_coordinates_np:
        dist = geodesic(pass_coord, destination_coordinate).kilometers
        return dist

# dictionary contaning the total distances for each route of each group
distance_dict = {}

# loop to calculate distance of each group from cab as well as destination and then calculating their total distance
for index, group_coordinate in enumerate(passenger_group_coordinates, start=1):

    # distance between destination and current location of group
    dist = find_destination_distance(group_coordinate, destination_coordinate_np)
    print('Group number %s distance from destination is %s km' %(index, int(dist)))

    # initialise dict keys with empty list
    distance_dict[index] = []
    for j, cab_location in enumerate(cab_coordinates_np, start=1):
        distance_from_car = geodesic(group_coordinate, cab_location).kilometers
        total_distance = distance_from_car + dist
        distance_dict[index].append(total_distance)
        print('Distance of group %s from car %s is %s' % (index, j, int(total_distance)))

# from the dictionary, find the minimum dist for each group and print that
for x, y in distance_dict.items():
    print('For group %s, the route with minimum distance is %s' % (x, int(min(y))))

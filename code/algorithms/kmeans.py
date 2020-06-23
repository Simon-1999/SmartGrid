import matplotlib.pyplot as plt
"""Divides a district in Kmeans clusters based on houses' distances to batteries.

The algorithm creates centroids for each battery in the district, and keeps modifying these to create a cluster
of houses with similar distances to a battery, and keeps this cluster as close to the battery as possible. 
"""

import numpy
import copy
import random

from .algorithm import Algorithm

class Kmeans(Algorithm):
    """Creates K-Means clusters in a district of the houses, each cluster belonging to one battery

    The K-Means algorithm starts by putting cluster centroids on the batteries' locations. Repeatedly, all houses are then assigned to their nearest
    centroid. After this, new centroids are being calculated by computing the mean. This is repeated until the centroids do not change any more. 

    Methods
    ----------
    run()
        Runs the algorithm

    make_connections(clusters)
        Assigns houses to each battery cluster

    get_nearest_cluster(clusters, house)
        Finds cluster centroid closest to a house

    calc_centroid(houses)
        Calculates centroid of a list of houses
    """

    def run(self):
        """Runs the K-Means sorting algorithm.

        Returns
        ----------
        District object
            K-Means distributed district
        """

        # initialize clusters
        clusters = []

        for battery in self.district.batteries:

            clusters.append({'centroid': battery.location, 'houses': [], 'battery': battery})

        # loop untill centroids don't change
        while True:
            self.iterations += 1

            # assign house to nearest centroid
            for house in self.district.houses:

                nearest_cluster = self.get_nearest_cluster(clusters, house)
                nearest_cluster['houses'].append(house) 

            # calculate new centroid
            centroids_changed = False

            # loop trough clusters
            for cluster in clusters:
                new_centroid = self.calc_centroid(cluster['houses'])
                old_centroid = cluster['centroid']

                # # track if centroid is changed
                if new_centroid != old_centroid:
                    centroids_changed = True
                    cluster['centroid'] = new_centroid
               
            # stop searching if convergence found
            if centroids_changed:
                for cluster in clusters:
                    cluster['houses'] = [] 
            else:
                break

        self.make_connections(clusters)
        
        return self.district, clusters


    def make_connections(self, clusters):
        """Creates connections between batteries and houses in the district when clusters are found.

        Parameters
        ----------
        clusters : list
            Clusters in the district
        """

        # make connections
        for cluster in clusters:
            
            houses = cluster['houses']
            battery = cluster['battery']

            for house in houses:
                self.district.add_connection(battery, house)
                  
                  
    def get_nearest_cluster(self, clusters, house):
        """Finds nearest cluster centroid to a house.

        Parameters
        ----------
        clusters : list
            Clusters in the district

        house : House object
        
        Returns
        ----------
        dict
        """

        min_dist = float('inf')

        nearest_cluster = None

        # loop trough clusters
        for cluster in clusters:
            
            dist = self.calc_dist(cluster['centroid'], house.location)
            # find the closest centroid 
            if dist < min_dist:
                min_dist = dist
                nearest_cluster = cluster

        return nearest_cluster


    def calc_centroid(self, houses):
        """Calculates centroid of a cluster

        Parameters 
        ----------
        houses : list
            Cluster represented by its assigned houses

        Returns
        ----------
        tuple
        """

        total_x = 0
        total_y = 0

        for house in houses:
            x_house, y_house = house.location
            total_x += x_house
            total_y += y_house
        
        return (float(total_x/len(houses)), float(total_y/len(houses)))
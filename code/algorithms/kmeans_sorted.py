"""Modifies a Kmeans-distributed district to have houses sorted based on their distance
to other districts 
"""

from itertools import chain
from .algorithm import Algorithm

class KmeansSorting(Algorithm):
    """Sorts houses in each cluster of a district based on their distance to the closest other cluster. 

    For each house, the algorithm determines its minimum distance to houses of other clusters. The houses in each cluster are sorted
    based on this distance, and a new, sorted district is returned. 

    Attributes
    ----------
    sort_district: District object
        District object that needs to be sorted
        
    clusters : list
        clusters in a District object

    Methods
    ----------
    run()
        Runs the sorting process

    dist_other_house(house, clusters)
        Calculates the distance of a house to the closest house of another cluster
    """

    def __init__(self, district, clusters):
        self.clusters = clusters
        self.sort_district = district


    def run(self):
        """Modifies a Kmeans-distributed district to have houses sorted based on their distance
        to other districts 

        Returns
        ----------
        District object
            A district in which the houses in each cluster are sorted 
        """

        # loop through every cluster
        for cluster in self.clusters:
            # sort the houses based on their distance to other clusters
            houses_sorted = sorted(cluster['houses'], key=lambda house: self.dist_other_house(house, self.clusters))
            battery = cluster['battery']

            self.sort_district.connections[battery.id] = houses_sorted
            # print(houses_sorted)
        
        return self.sort_district
    
    
    def dist_other_house(self, house, clusters):
        """Returns distance of a house to the closest house of another cluster.

        Parameters
        ----------
        house : House object
            House to calculate distance to other clusters from
        clusters: list
            Existing clusters in a district

        Returns
        ----------
        int
            Distance to closest house of another cluster
        """
        
        min_dist = float('inf')
        other_houses_lists = []

        for cluster in clusters: 
            # skip own cluster from calculations
            if house in cluster['houses']:
                continue
            
            # add all the other houses to the list
            other_houses_lists.append(cluster['houses'])

            # flatten the list of other houses since ATM it consists of lists per cluster
            other_houses = list(chain(*other_houses_lists))
        
        for other_house in other_houses:
            if self.calc_dist(house.location, other_house.location) < min_dist:
                min_dist = self.calc_dist(house.location, other_house.location)
        
        return min_dist

import matplotlib.pyplot as plt
import numpy
import copy
import random

from .algorithm import Algorithm

class Kmeans(Algorithm):

    def run(self):
        
        print("Kmeans running... ")

        min_costs = float('inf')

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

        self.plot_cluster(self.district, clusters)

        self.make_connections(clusters)
        self.print_result(self.district)

        print("Kmeans done")
        
        return self.district, clusters

    def make_connections(self, clusters):

        # make connections
        for cluster in clusters:
            
            houses = cluster['houses']
            battery_id = cluster['battery'].id

            for house in houses:
                self.district.connections[battery_id].append(house)
                  
    def get_nearest_cluster(self, clusters, house):

        min_dist = float('inf')

        nearest_cluster = None

        # loop trough clusters
        for cluster in clusters:
            
            dist = self.calc_dist(cluster['centroid'], house.location)

            if dist < min_dist:
                min_dist = dist
                nearest_cluster = cluster

        return nearest_cluster

    def calc_centroid(self, houses):

        total_x = 0
        total_y = 0

        for house in houses:
            x_house, y_house = house.location
            total_x += x_house
            total_y += y_house
        
        return (float(total_x/len(houses)), float(total_y/len(houses)))

    def plot_cluster(self, district, clusters):

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1) 
        plt.title(f'Kmeans clustering of district{district.id}')

        color = {0: "blue", 1:"red" ,2:"yellow",3:"cyan", 4:"magenta"} 

        for cluster in clusters:  
            for house in cluster['houses']:            
                x, y = house.location
                plt.plot(x, y, 'p', color=color[cluster['battery'].id], markersize=7)

            x, y = cluster['centroid']
            plt.plot(x, y, 'k+', markersize=25)

        # loop through batteries
        for battery in district.batteries:
            x, y = battery.location
            plt.plot(x, y, 'ks', label = f'battery{battery.id}', color=color[battery.id], markersize=10, alpha=0.5)

        # plot district  
        ax.set_xticks(numpy.arange(0, 51, 1), minor=True)
        ax.set_yticks(numpy.arange(0, 51, 1), minor=True)
        ax.grid(which='minor', alpha=0.2)
        plt.legend()
        plt.show()

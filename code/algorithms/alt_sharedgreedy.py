import copy
import random
import matplotlib.pyplot as plt
import numpy

from .algorithm import Algorithm

class SharedGreedy(Algorithm):

    def __init__(self, district):

        self.district = district
        self.free_houses = []
        self.iterations = 0

        # connectpoints {BATTERY_ID: [LOCATION, LOCATION, LOCATION]}
        self.connectpoints = self.init_connectpoints()
        # cables {HOUSE_ID: [LOCATION, LOCATION, LOCATION]}
        self.cables = {}

    def run(self):

        print("SharedGreedy running... ")

        self.connectpoints = self.init_connectpoints()
        self.cables = {}

        costs = 0
        #Loop through the districts

        for i in range(3):
            # loop through batteries
            for battery in self.district.batteries:

                houses = self.district.connections[battery.id]

                # sort houses from on distance from battery
                houses.sort(key=lambda house: self.calc_dist(house.location, battery.location))

                # loop through houses
                for house in houses:

                    # find nearest connectpoint
                    connectpoint = self.get_nearest_connectpoint(battery, house)   
                
                    # check if house has a path, if not make path
                    if house.id not in self.cables:
                        # make cable path
                        path = self.get_cable_path(house.location, connectpoint)
                        print(path)
                        self.cables[house.id] = path

                        # add path to connectpoints
                        for point in path:
                            self.connectpoints[battery.id].append(point)
                    else:
                        path = self.cables[house.id]
    
                        path_len = len(self.cables[house.id])# -1?
                        dist = self.calc_dist(house.location, connectpoint)

                        if dist < path_len:

                            #print("shorter")
                            #remove current path connectpoints
                            #for point in path:
                                #self.connectpoints[battery.id].remove(point)
                            

                            #add new path
                            path = self.get_cable_path(house.location, connectpoint)
                            print(path)
                        self.cables[house.id] = path

                        # add path to connectpoints
                        for point in path:
                            self.connectpoints[battery.id].append(point)
            # plot cables
            print("NEW CONFIG")
            print(len(self.cables))
            self.plot_cables(self.district)

        print("SharedGreedy done ")

    def get_nearest_connectpoint(self, battery, house):

        #remove house path/connectpoints from the list
        if house.id in self.cables:
            path = self.cables[house.id]

            for point in path:
                self.connectpoints[battery.id].remove(point)


        return min(self.connectpoints[battery.id], key=lambda \
            location: self.calc_dist(location, house.location))

    def get_cable_path(self, start_location, end_location):

        # unpack location
        current_x, current_y = start_location
        end_x, end_y = end_location

        # initialize path
        path = [(current_x, current_y)] 

        # get movement direction
        hor_dist = end_x - current_x
        if abs(hor_dist) > 0:
            hor_move = int(hor_dist / abs(hor_dist))
        ver_dist = end_y - current_y    
        if abs(ver_dist) > 0:
            ver_move = int(ver_dist / abs(ver_dist))

        # initialize movements list
        movements = []

        # add horizontal movements 
        for x in range(abs(hor_dist)):
            movements.append((hor_move, 0))
        
        # add vertical movements to list
        for y in range(abs(ver_dist)):
            movements.append((0, ver_move))

        # shuffle list of movements
        random.shuffle(movements)

        # make path
        for movement in movements:

            # extract movement
            move_x, move_y = movement

            # increment current position
            current_x += move_x
            current_y += move_y

            # add position to path
            path.append((current_x, current_y))

        return path 

    def init_connectpoints(self):

        connectpoints = {}

        for battery in self.district.batteries:

            connectpoints[battery.id] = [battery.location]

        return connectpoints

    def plot_cables(self, district):

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1) 
        plt.title(f'District{district.id}')

        color = {0: "blue", 1:"red" ,2:"yellow",3:"cyan", 4:"magenta"} 

        # loop through batteries
        for battery in district.batteries:
            x, y = battery.location
            plt.plot(x, y, 'ks', label = f'battery{battery.id}', color=color[battery.id], markersize=10)

            for house in district.connections[battery.id]:             
                x, y = house.location
                plt.plot(x, y, 'p', color=color[battery.id], markersize=7, alpha=0.5)

                path_x = []
                path_y = []

                for path in self.cables[house.id]:
                    x, y = path
                    path_x.append(x)
                    path_y.append(y)
                
                #print(path_x)
                #print(path_y)

                plt.plot(path_x, path_y, '-', color=color[battery.id], alpha=0.3)

        # plot district  
        ax.set_xticks(numpy.arange(0, 51, 1), minor=True)
        ax.set_yticks(numpy.arange(0, 51, 1), minor=True)
        ax.grid(which='minor', alpha=0.2)
        plt.legend()
        plt.show()
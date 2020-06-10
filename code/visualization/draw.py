import matplotlib.pyplot as plt
import numpy

def plot(district):
    """ 
    Draw grid with houses, batteries and connections
    """

    color = {0: "blue", 1:"red" ,2:"yellow",3:"cyan", 4:"magenta"}

    # configure plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.title(f'District{district.id}') 

    # loop through batteries
    for battery in district.get_batteries():
        x, y = battery.get_location()
        plt.plot(x, y, 's', label = f'battery{battery.id}', markersize=10, \
            color=color[battery.id])

    # coordinate lists for houses
    x_houses = []
    y_houses = []

    # loop through houses
    for house in district.get_houses():
        x, y = house.get_location()
        x_houses.append(x)
        y_houses.append(y)

    # loop through cables
    for cable in district.cables:

        x_path = []
        y_path = []

        # add coordinates of path to x_path and y_path
        for location in cable.path:

            x, y = location
            x_path.append(x)
            y_path.append(y)
      
        # add cable path to plot
        plt.plot(x_path, y_path, "-", color=color[cable.battery.id])

    # plot district    
    plt.plot(x_houses, y_houses, 'kp', label = 'house', markersize=7)
    ax.set_xticks(numpy.arange(0, 51, 1), minor=True)
    ax.set_yticks(numpy.arange(0, 51, 1), minor=True)
    ax.grid(which='minor', alpha=0.2)
    plt.legend()
    plt.show()
    
import matplotlib.pyplot as plt
import numpy

def plot_cables(district):
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
        x, y = battery.location
        plt.plot(x, y, 's', label = f'battery{battery.id}', markersize=10, \
            color=color[battery.id])
        # plt.text(x + 0.4, y - 0.2, f"{battery.usage:.1f}", fontsize=8)

    # loop through houses
    for house in district.get_houses():
        x, y = house.location
        plt.plot(x, y, 'kp', markersize=7)
        # plt.text(x + 0.2, y + 0.2, f"{house.output:.0f}", fontsize=8)

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
        plt.plot(x_path, y_path, "-", color=color[cable.battery.id], alpha=0.3)

    # plot district    
    ax.set_xticks(numpy.arange(0, 51, 1), minor=True)
    ax.set_yticks(numpy.arange(0, 51, 1), minor=True)
    ax.grid(which='minor', alpha=0.2)
    plt.legend()
    plt.show()

def plot_connections(district):

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

    # plot district  
    ax.set_xticks(numpy.arange(0, 51, 1), minor=True)
    ax.set_yticks(numpy.arange(0, 51, 1), minor=True)
    ax.grid(which='minor', alpha=0.2)
    plt.legend()
    plt.show()
    
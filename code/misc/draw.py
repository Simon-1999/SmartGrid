import matplotlib.pyplot as plt
import numpy

def plot(district):
    """ 
    Draws grid with houses, batteries and connections, color-coded. 

    Parameters
    ----------
    district : District object
    """

    color = {0: "blue", 1:"red" ,2:"green",3:"cyan", 4:"magenta"}

    # configure plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.title(f'District {district.id}') 

    # loop through batteries
    for battery in district.batteries:
        x, y = battery.location
        plt.plot(x, y, 's', label = f'battery{battery.id}', markersize=10, \
            color=color[battery.id])

        # loop through houses
        for house in district.connections[battery.id]:
            x, y = house.location
            plt.plot(x, y, 'p', markersize=7, color=color[battery.id])

            # plot path if house has a cable
            if house.id in district.cables:

                # save cable path in list
                x_path = []
                y_path = []
                for location in district.cables[house.id]:
                    x, y = location
                    x_path.append(x)
                    y_path.append(y)

                # plot path
                plt.plot(x_path, y_path, '-', color=color[battery.id], alpha=0.8)
 
    ax.set_xticks(numpy.arange(0, 51, 1), minor=True)
    ax.set_yticks(numpy.arange(0, 51, 1), minor=True)
    ax.grid(which='minor', alpha=0.2)
    plt.legend()
    plt.show()
    
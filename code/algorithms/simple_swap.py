import numpy as np

def simple_swap(config_district):
    """
    Optimizing solution found by Manhattan distance based configuration, 
    based on the swapping of similar houses to a closer battery.
    """

    print("========== optimizing (simple_swap algorithm) ===========")

    # extract the longest cables
    longest_list = select_longest_cables(config_district.cables)
        
    


    # 
    pass

def select_longest_cables(cables):
    # select the longest 25% of the cables
    cables_list = []

    for cable in cables:
        cable_length = cable.calc_length()

        # append the cable object with its length to the list
        cables_list.append((cable, cable_length))

    # sort list based on length and extract the longest 25%
    return sorted(cables_list, key=lambda cable: cable[1], reverse=True)[:len(cables_list // 4)]

def useful_swap():
    return False

def swap():
    pass
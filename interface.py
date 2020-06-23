from code import classes, algorithms, visualization

import os
# os.system('cls||clear')

class Interface():

    def __init__(self):

        self.init_algorithms()

    def load_district(self, uid):
        """
        Initializes district objects for all three districts
        """

        print('status: loading district...')

        # file pathways
        batteries_file = f"data/district_{uid}/district-{uid}_batteries.csv"
        houses_file = f"data/district_{uid}/district-{uid}_houses.csv"

        district = classes.District(uid, batteries_file, houses_file)

        print('status: loaded district')

        return district

    def init_algorithms(self):

        # aks for district id
        message = 'Choose district 1, 2 or 3 \n'
        options = ['1', '2', '3']
        district_id = int(self.input_validation(options, message))
        district = self.load_district(district_id)

        # ask for unique or shared cables
        message = "Type u for unique cables or s for shared cables\n"
        options = ['u', 's']
        cable_type = self.input_validation(options, message)

        print('status: loading algorithms...')

        if cable_type == 'u':

            self.algorithms = {
                'initial': 
                {

                    'r': {'name': 'Randomized', \
                        'description': 'Randomly shuffles houses list and assign houses to battery untill valid configuration is found', \
                        'class': algorithms.Randomize(district), \
                        'optimizations': ['s']},
                    'ro': {'name': 'RandomOptimize', \
                        'description': 'Randomly shuffles houses list and assign house to nearest free battery untill valid configuration is found', \
                        'class': algorithms.RandomOptimize(district), \
                        'optimizations': ['s']},
                    'l': {'name': 'Lowerbound', \
                        'description': 'Assign house to nearest battery', \
                        'class': algorithms.LowerBound(district), \
                        'optimizations': []},
                    'u': {'name': 'UpperBound', \
                        'description': 'Assign house to farest battery', \
                        'class': algorithms.UpperBound(district), \
                        'optimizations': []}
                },
                'optimization':
                {
                    's': {'name': 'SimpleSwap', \
                        'description': 'Swaps cables with similar output house untill no swaps possible', \
                        'class': algorithms.SimpleSwap(district), \
                        'optimizations': []},
                    'g': {'name': 'GroupSwap', \
                        'description': 'Swaps longest cables in groups', \
                        'class': algorithms.GroupSwap(district), \
                        'optimizations': []}
                }
            } 

        if cable_type == 's':

            # run kmeans and kmeans sorting
            district, clusters = algorithms.Kmeans(district).run()
            district = algorithms.KmeansSorting(district, clusters).run()

            self.algorithms = {
                'initial': 
                {
                    'cc': {'name': 'ConfigFinderCosts', \
                        'description': 'Removes closest neighbours with capacity offset, random shuffles removed houses and connects them to closest free battery', \
                        'class': algorithms.ConfigFinderCosts(district, clusters), \
                        'optimizations': ['rs', 's']},
                    'cl': {'name': 'ConfigFinderLength', \
                        'description': 'Removes closest neighbours with capacity offset, random shuffles removed houses and connects them to closest free battery', \
                        'class': algorithms.ConfigFinderLength(district, clusters), \
                        'optimizations': ['rs', 's']},
                    'dc': {'name': 'DepthFirstCost', \
                        'description': 'Removes closest neighbours with capacity offset, random shuffles removed houses and builds children with closest neighbour', \
                        'class': algorithms.DepthFirstCosts(district), \
                        'optimizations': ['rs', 's']},
                    'dl': {'name': 'DepthFirstLength', \
                        'description': 'Removes closest neighbours with capacity offset, random shuffles removed houses and builds children with closest neighbour', \
                        'class': algorithms.DepthFirstLength(district, clusters), \
                        'optimizations': ['rs', 's']}
                },
                'optimization':
                {
                    'rs': {'name': 'RandomSharedGreedy', \
                        'description': 'Make random pathways to nearest connectpoint and save lowest cost configuration', \
                        'class': algorithms.RandomSharedGreedy(district), \
                        'optimizations': []},
                    's': {'name': 'SharedGreedy', \
                        'description': 'Make pathway from house to nearest connectpoint', \
                        'class': algorithms.SharedGreedy(district), \
                        'optimizations': []}
                }
            } 

        print('status: algorithms loaded')

    # def init_unique_algorithms(self):

    #     return {
    #         'initial': 
    #         {

    #             'r': {'name': 'Randomized', \
    #                 'description': 'Randomly shuffles houses list and assign houses to battery untill valid configuration is found', \
    #                 'class': algorithms.Randomize(district), \
    #                 'optimizations': ['s']},
    #             'ro': {'name': 'RandomOptimize', \
    #                 'description': 'Randomly shuffles houses list and assign house to nearest free battery untill valid configuration is found', \
    #                 'class': algorithms.RandomOptimize(district), \
    #                 'optimizations': ['s']},
    #             'l': {'name': 'Lowerbound', \
    #                 'description': 'Assign house to nearest battery', \
    #                 'class': algorithms.LowerBound(district), \
    #                 'optimizations': []},
    #             'u': {'name': 'UpperBound', \
    #                 'description': 'Assign house to farest battery', \
    #                 'class': algorithms.UpperBound(district), \
    #                 'optimizations': []},                               
    #             'k': {
    #                 'name': 'Kmeans', \
    #                 'description': 'Cluster houses with kmeans clustering and sort houses from close to far from another cluster', \
    #                 'class': algorithms.Kmeans(district), \
    #                 'optimizations': ['c', 'd']}
    #         },
    #         'optimization':
    #         {
    #             's': {'name': 'SimpleSwap', \
    #                 'description': 'Swaps cables with similar output house untill no swaps possible', \
    #                 'class': algorithms.SimpleSwap(district), \
    #                 'optimizations': []},
    #             'g': {'name': 'GroupSwap', \
    #                 'description': 'Swaps longest cables in groups', \
    #                 'class': algorithms.GroupSwap(district), \
    #                 'optimizations': []}
    #         }
    #     } 

    # def init_shared_algorithms(self):

    #     return {
    #         'initial': 
    #         {

    #             'r': {'name': 'Randomized', \
    #                 'description': 'Randomly shuffles houses list and assign houses to battery untill valid configuration is found', \
    #                 'class': algorithms.Randomize(district), \
    #                 'optimizations': ['s']},
    #             'ro': {'name': 'RandomOptimize', \
    #                 'description': 'Randomly shuffles houses list and assign house to nearest free battery untill valid configuration is found', \
    #                 'class': algorithms.RandomOptimize(district), \
    #                 'optimizations': ['s']},
    #             'l': {'name': 'Lowerbound', \
    #                 'description': 'Assign house to nearest battery', \
    #                 'class': algorithms.LowerBound(district), \
    #                 'optimizations': []},
    #             'u': {'name': 'UpperBound', \
    #                 'description': 'Assign house to farest battery', \
    #                 'class': algorithms.UpperBound(district), \
    #                 'optimizations': []},                               
    #             'k': {
    #                 'name': 'Kmeans', \
    #                 'description': 'Cluster houses with kmeans clustering and sort houses from close to far from another cluster', \
    #                 'class': algorithms.Kmeans(district), \
    #                 'optimizations': ['c', 'd']}
    #         },
    #         'optimization':
    #         {
    #             's': {'name': 'SimpleSwap', \
    #                 'description': 'Swaps cables with similar output house untill no swaps possible', \
    #                 'class': algorithms.SimpleSwap(district), \
    #                 'optimizations': []},
    #             'g': {'name': 'GroupSwap', \
    #                 'description': 'Swaps longest cables in groups', \
    #                 'class': algorithms.GroupSwap(district), \
    #                 'optimizations': []}
    #         }
    #     } 

    def run(self):
        """
        Runs the interface
        """

        # get algorithm and run it
        algorithm = self.initial_choice()  
        self.algorithm_run(algorithm)

        # loop unitil no optimizations left
        while len(algorithm['optimizations']) > 0:
            
            # get algorithm and run it
            algorithm = self.optimization_choice(algorithm)
            self.algorithm_run(algorithm)

        print("Interface closed")

    def input_validation(self, options, message):
        """
        Validation of input
        """

        while True:

            user_input = input(message)

            if user_input in options:
                return user_input

            print('error: invalid input')

    def optimization_choice(self, algorithm):
        """
        Choose optimization algorithm
        """

        print("Choose optimization algorithm")

        # get algorithm shortcut
        message = ''
        options = []
        for shortcut in algorithm['optimizations']:

            opt_algorithm = self.algorithms['optimization'][shortcut]

            message += self.get_message(shortcut, opt_algorithm)
            options.append(shortcut)

        shortcut = self.input_validation(options, message)

        # return algorithm dictionary
        return self.algorithms['optimization'][shortcut]

    def initial_choice(self):
        """
        Choose initial algorithm
        """

        print("Choose initial algorithm")

        # ask for algorithm
        message = ''
        options = []
        for shortcut, algorithm in self.algorithms['initial'].items():

            message += self.get_message(shortcut, algorithm)
            options.append(shortcut)

        shortcut = self.input_validation(options, message)

        # return algorithm dictionary
        return self.algorithms['initial'][shortcut]

    def algorithm_run(self, algorithm):
        """
        Run algorithm
        """
 
        print(f"status: running {algorithm['name']}...")

        district = algorithm['class'].run()

        print(f"status: {algorithm['name']} is finished")

        # show cost scheme and visualization of cables
        district.print_district_status()
        visualization.draw.plot(district)

        # aks for making outputfile
        #TODO     

    def get_message(self, shortcut, algorithm):

        return 'Type ' + shortcut + ' for ' + algorithm['name'] + '\n' + algorithm['description'] + '\n'
    
    def int_conv(self, integer):
        """
        Convert integers 1 and 0 to strings Yes and No
        """

        if integer == 1:
            return 'Yes'
        else:
            return 'No'

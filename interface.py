"""Interface for running all algorithms. User gets asked for district and cable type and can choose
which algorithm to run.
"""

from code import classes, algorithms, misc
import os

class Interface():
    """This class upholds a structure for the interface when running main.py

    Methods
    ----------
    load_district(uid)
        Initialize district object

    init_unique_algorithms(district)
        Makes dictionary of all unique algorithms with information and classes

    init_shared_algorithms(district)
        Makes dictionary of all shared algorithms with information and classes
    
    run()
        Runs the interface

    input_validation(options, message)
        Asks for input with message and checks if input is in options

    optimization_choice(algorithm)
        Generete options for optimization algorithms

    initial_choice()
        Generete options for initial algorithms

    algorithm_run(algorithm)
        Runs algorithm and shows result

    get_message(algorithm)
        Generates string for command instructions and info of algorithm

    """

    def __init__(self):

        # ask for district id
        message = 'Choose district 1, 2 or 3 \n'
        options = ['1', '2', '3']
        district_id = int(self.input_validation(options, message))
        district = self.load_district(district_id)

        # ask for unique or shared cables
        message = "Type u for unique cables or s for shared cables\n"
        options = ['u', 's']
        cable_type = self.input_validation(options, message)

        os.system('cls||clear')
        print('status: loading algorithms...')

        if cable_type == 'u':
            self.algorithms = self.init_unique_algorithms(district)
            self.shared = False

        if cable_type == 's':
            self.algorithms = self.init_shared_algorithms(district)
            self.shared = True

        os.system('cls||clear')
        print('status: algorithms loaded')

    def load_district(self, uid):
        """
        Initializes district object

        Parameters
        ----------
        uid: int

        Returns
        ----------
        District object
        """

        os.system('cls||clear')
        print('status: loading district...')

        # make district object
        batteries_file = f"data/district_{uid}/district-{uid}_batteries.csv"
        houses_file = f"data/district_{uid}/district-{uid}_houses.csv"
        district = classes.District(uid, batteries_file, houses_file)

        os.system('cls||clear')
        print('status: loaded district')

        return district

    def init_unique_algorithms(self, district):
        """
        Makes dictionary of all unique algorithms with information and classes
        
        Parameters
        ----------
        district: object

        Returns
        ----------
        dict 
        """

        return {
            'initial': 
            {

                'r': {'name': 'Randomized', \
                    'description': 'Randomly shuffles houses list and assign houses to battery untill valid configuration is found', \
                    'class': algorithms.Randomize(district), \
                    'optimizations': ['s', 'g']},
                'ro': {'name': 'RandomOptimize', \
                    'description': 'Randomly shuffles houses list and assign house to nearest free battery untill valid configuration is found', \
                    'class': algorithms.RandomOptimize(district), \
                    'optimizations': ['s', 'g']},
                'l': {'name': 'Lowerbound', \
                    'description': 'Assign house to nearest battery', \
                    'class': algorithms.LowerBound(district), \
                    'optimizations': []},
                'u': {'name': 'UpperBound', \
                    'description': 'Assign house to farest battery', \
                    'class': algorithms.UpperBound(district), \
                    'optimizations': []},                               
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

    def init_shared_algorithms(self, district):
        """
        Makes dictionary of all shared algorithms with information and classes
       
        Parameters
        ----------
        district: object

        Returns
        ----------
        dict
        """

        district, clusters = algorithms.Kmeans(district).run()
        district = algorithms.KmeansSorting(district, clusters).run()

        return {
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

    def run(self):
        """
        Runs the interface
        """

        # get initial algorithm and run it
        algorithm = self.initial_choice()  
        self.algorithm_run(algorithm)

        # loop untill no optimizations left
        if len(algorithm['optimizations']) > 0:
            
            # get algorithm and run it
            algorithm = self.optimization_choice(algorithm)
            self.algorithm_run(algorithm)       

        print("Interface closed")

    def input_validation(self, options, message):
        """
        Asks for input with message and checks if input is in options

        Parameters
        ----------
        options: list
        message: str

        Returns
        ----------
        str
        """

        while True:

            user_input = input(message)

            if user_input in options:
                return user_input

            print('error: invalid input')

    def optimization_choice(self, algorithm):
        """
        Generete options for optimization algorithms
        
        Parameters
        ----------
        algorithm: dict

        Returns
        ----------
        dict 
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
        Generete options for initial algorithms

        Returns
        ----------
        dict
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
        Runs algorithm and shows result

        Parameters
        ----------
        algorithm: dict
        """
 
        os.system('cls||clear')
        print(f"status: running {algorithm['name']}...")

        district = algorithm['class'].run()

        os.system('cls||clear')
        print(f"status: {algorithm['name']} is finished")

        # show cost scheme and visualization of cables
        district.print_district_status()
        misc.plot(district)

        # aks for making outputfile
        message = 'Do you want to generate an output file y/n \n'
        options = ['y', 'n']
        if self.input_validation(options, message) == 'y':
            misc.output_doc(district, self.shared) 

    def get_message(self, shortcut, algorithm):
        """
        Generates string for command instructions and info of algorithm

        Parameters
        ----------
        shortcut: string
        algorithm: dict

        Returns
        ----------
        str
        """
        
        return '\nType ' + shortcut + ' for ' + algorithm['name'] + '\n' + algorithm['description'] + '\n'
    
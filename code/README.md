# SmartGrid Code

AN overview of all code of our SmartGrid project.

## Structure

The following list describes the most important folders and files in the *code* folder, for easy navigation.

- **/algorithms**: contains almost all code for the project
  - **/algorithms/algorithm.py**
  - **/algorithms/config_finder_costs.py**
  - **/algorithms/config_finder_length.py**
  - **/algorithms/group_swap.py**
  - **/algorithms/kmeans.py**
  - **/algorithms/kmeans_depth_first_costs.py**
  - **/algorithms/kmeans_depth_first_length.py**
  - **/algorithms/kmeans_sorted.py**
  - **/algorithms/lowerbound.py**
  - **/algorithms/random_opt.py**
  - **/algorithms/random_sharedgreedy.py**
  - **/algorithms/randomize.py**
  - **/algorithms/sharedgreedy.py**
  - **/algorithms/simple_swap.py**
  - **/algorithms/upperbound.py**
- **/classes**
  - **/classes/battery.py**
  - **/classes/district.py**
  - **/classes/house.py**
- **/visualization**
  - **/visualization/draw.py**
  - **visualization/loadconnections.py**
  - **visualization/make_output.py**

## Classes

### District

This is the umbrella class that keeps track of the whole district, its houses and batteries, connections and cables. An important distinction is to be made here: a *connection* describes that a house 'belongs to' a battery, but it might not yet have been physically connected yet. These are described by the *cables*. 

### Battery

This class represents the batteries in the district. 

### House

This class represents the houses in the district. 

## Algorithms

All algorithms are defined as classes that inherit from one umbrella *Algorithm* class to keep track of general aspects, such as the district and the amount of iterations. 

### Upper- and lowerbound

These algorithms are used to calculate the upper- and lowerbound of the costs of a district. We can review any other algorithm's results with this even if we do not have comparisons inbetween algorithms. 

### Randomize and Random Optimization

These are algorithms for a district where houses *can not* share cables and each house has its own connection to a battery. 

The **Randomize** algorithm shuffles the houses in a district and then adds them one by one to the battery that has the most available capacity, until it has found a valid configuration.

**RandomOptimization** kind of does the same thing, but also uses the distance to a battery to make sure each house picks its best option.

### Simple Swap and Group Swap

These are algorithms for a district where houses *can not* share cables and each house has its own connection to a battery. 

**SimpleSwap** repeatedly takes the longest connection from a configurated district and checks if there's a possibility for a swap with a similar house, that is connected to another battery. If a swap results in less needed cables, houses are swapped regarding their batteries. 

**GroupSwap** has a different way of optimizing. It takes a group of connections that are the longest of the whole configuration, and then repeatedly takes a random sample of this group. If a random reassignment of these cables results in a cheaper configuration, this new configuration is remembered. This continues for a set amount of iterations and multiple group sizes. 

### K-Means Clustering

When given a raw district, the **Kmeans** algorithm creates clusters of houses based on their distances to the batteries. All houses within a cluster have a similar distance to 'their' battery. After this clustering, optimization algorithms can be performed to create a valid, relatively cheap configuration.

As an elaboration, there is a **KmeansSorting** algorithm. This determines which houses are on the border of their clusters and actually closer to other clusters than their own centroid. Houses that are on borders appear on the front of a cluster's houses list. 

### K-Means Depth First

After creating a sorted K-Means distributed district, we have developed a pruned depth first search for an optimal configuration. With a hard-coded capacity offset, 'border' houses are disconnected from their batteries. On this collection of border houses, a depth first search is performed. Every time children are build (i.e. five battery options per house), the two best options are taken into account. If we tried to do a full depth first search of this process, the algorithm took way too long, so we chose for this pruning method. Even now, running still takes several hours.

There are two versions of optimization. **DepthFirstLength** reviews configurations based on the length of the longest connection and tries to minimize this. **DepthFirstCosts** reviews configurations based on total district costs. 

### Configuration Finder

The **ConfigFinder** algorithm searches for a distribution of a district's houses among the batteries. Just like the depth first algorithm, there are two versions of optimization: **ConfigFinderLength** and **ConfigFinderCosts**, that minimize length of the longest connection and total district costs respectively. 

Both algorithms disconnect border houses (determined by **KmeansSorting**) until a certain capacity offset at a battery. Then, new connections to other batteries are connected by finding the closest available battery. If a new configuration has a better score than the previous one, it is remembered. 

### Shared Greedy and Random Shared Greedy

These are algorithms for a district where houses *can* share cables. We aim to use a district that has already been distributed by for example K-Means clustering.

**SharedGreedy** initializes a district's batteries as so-called *connectpoints*. It then loops through all houses that are assigned to that battery and connects each house to the nearest connectpoint. After a house has a cable that directly or indirectly leads to a battery, the house's path is added to the connectpoints. The next house then connects to the closest connectpoint again. This way houses create a network that connects everything to a battery. 

**RandomSharedGreedy** is actually multiple runs of the **SharedGreedy** algorithm. After having performed one run of **SharedGreedy**, it reviews all connections and checks whether a better option has formed after new houses have been connected.

## Visualization

These modules process the output generated by the performed algorithm(s).

### Output

The final District object that is returned after all called algorithms have run is translated into a JSON-file called *output.json*.

### Draw

A district is plotted with color-coding of houses and the batteries they are connected to with the cables. 

### Load connections

Since our depth first algorithms take a very long runtime, we have saved some of the configurations we found in our own runs. If you wish to visualize these results without having to wait for a depth first algorithm to have finished, you can use this module to create a visualization without actually running the algorithm.
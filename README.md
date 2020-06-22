# SmartGrid

### Project for University of Amsterdam course *Programmeertheorie / Heuristieken*

When using green energy, sources like solar panels or windmills often produce more than necessary. Luckily, this surplus can be stored in batteries. 

In a district with houses that produce output and batteries that have a capacity, cables
can be used to connect all houses to batteries. These cables can either be added uniquely, i.e. every house has its own cable to a battery, or they can be shared between houses. 

Of course it costs money to build such a network of cables and also to place batteries in a house district. This code tries to minimize the costs for a district wanting to have a so-called SmartGrid, by trying to minizime the amount of cables needed to connect all houses to a battery without exceeding capacity. 

## Requirements

This code is written in Python 3. The file `requirements.txt` lists all necessary packages
to succesfully run the program. These can easily be installed using `pip3` with the command

```pip3 install -r requirements.txt```

or using `conda` with the command 

```conda install --file requirements.txt```

## Usage

An interactive interface is started when running the following command:

`python3 main.py`

........UITLEG INTERFACE...........

## Structure

The following list describes the most important folders and files in the project, for easy
navigation.

- **/code**: contains almost all code for the project
  - **/code/algorithms**: contains code for all the algorithms
  - **/code/classes**: contains the three representation classes of the SmartGrid district
  - **/code/visualization**: contains code for plotting and writing output
- **/data**: contains data folders for the districts
- **/main.py**: code to run the full program in an interactive way, with a possibility to choose which algorithm to use.

## Authors
[Simon van Eeden](mailto:simonveeden@hotmail.com)  
[Hendrik Scheeres](mailto:hscheeresyt@gmail.com)  
[Noah van de Bunt](mailto:noahvandebunt@outlook.com)

June 2020, Amsterdam

## Acknowledgements

Many thanks to our supervisors Jasper den Duijf and Okke van Eck for all their good advice, critique and motivational moments. 
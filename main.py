from code import classes, algorithms, visualization

if __name__ == "__main__":

    # district id
    uid = 1

    # file pathways
    batteries_file = f"data/district_{uid}/district-{uid}_batteries.csv"
    houses_file = f"data/district_{uid}/district-{uid}_houses.csv"

    # make a test district to print
    test_district = classes.District(uid, batteries_file, houses_file)

    kmeans_district, clusters = algorithms.Kmeans(test_district).run()
    kmeans_sorted = algorithms.KmeansSorting(kmeans_district, clusters).run()

    print('18')
    configuration = algorithms.ConfigFinder(kmeans_sorted, clusters).run()
    print('19')

    # print the number of cables to check
#     print(len(test_district.cables))

    # return the total cost of the district
    costs = test_district.calc_connection_costs()
    total = costs["total"]
    cables = costs["connections"]
    batteries = costs["batteries"]

    # draw plot
  #  draw.plot(test_district)

    print(f"Total cost of the district:{total}")
    print(f"Total cost of the cables:{cables}")
    print(f"Total cost of the batteries:{batteries}")
from code.classes import district

if __name__ == "__main__":

    # district id
    uid = 1

    # file pathways
    batteries_file = f"data/district_{uid}/district-{uid}_batteries.csv"
    houses_file = f"data/district_{uid}/district-{uid}_houses.csv"

    # make a test district to print
    test_district = district.District(uid, batteries_file, houses_file)

    # print the batteries and houses
    print("BATTERIES")

    for battery in test_district.batteries:
        print(battery)

    print("HOUSES")

    for house in test_district.houses:
        print(house)

    print("=======================")

    test_house = test_district.get_houses()[0]
    test_batt = test_district.get_batteries()[0]

    test_district.add_cable(test_batt, test_house)

    test_cable = test_district.cables[0]

    print(test_cable.path)

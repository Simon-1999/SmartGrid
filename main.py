from code.classes import district
from code.algorithms import randomize

if __name__ == "__main__":

    # district id
    uid = 1

    # file pathways
    batteries_file = f"data/district_{uid}/district-{uid}_batteries.csv"
    houses_file = f"data/district_{uid}/district-{uid}_houses.csv"

    # make a test district to print
    test_district = district.District(uid, batteries_file, houses_file)

    # run random algorithm
    randomize.random_solution(test_district)
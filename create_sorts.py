from lib.sorters.cube_sorter import CubeSorter

sorter = CubeSorter()

steps = 10

r = range(-steps, steps + 1, 1)

for x in r:
    for y in r:
        for z in r:
            sorter.create((x / steps, y / steps, z / steps))


orderings = {}

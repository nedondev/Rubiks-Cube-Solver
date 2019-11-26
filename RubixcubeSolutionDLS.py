from ScrambleRubixcube import xInitial, make_move
import numpy as np
from datetime import datetime
import time


class State:
    cube = None
    cost = 0
    parent = None
    move = None


# checks if goal reached. if reached writes goal state in output.txt
def goal_reached(cube):
    for ref in [0, 3, 6, 9, 12, 15]:
        first = cube[ref, 0]
        for i in range(3):
            for j in range(3):
                if first != cube[ref + i, j]:
                    return False

    # goal reached
    file = open('output.txt', 'w')
    file.write("              " + str(cube[0, 0:3]) + '\n')
    file.write("              " + str(cube[1, 0:3]) + '\n')
    file.write("              " + str(cube[2, 0:3]) + '\n')
    file.write(str(cube[3, 0:3]) + ' ' + str(cube[6, 0:3]) + ' ' + str(cube[9, 0:3]) + ' ' + str(cube[12, 0:3]) + '\n')
    file.write(str(cube[4, 0:3]) + ' ' + str(cube[7, 0:3]) + ' ' + str(cube[10, 0:3]) + ' ' + str(cube[13, 0:3]) + '\n')
    file.write(str(cube[5, 0:3]) + ' ' + str(cube[8, 0:3]) + ' ' + str(cube[11, 0:3]) + ' ' + str(cube[14, 0:3]) + '\n')
    file.write("              " + str(cube[15, 0:3]) + '\n')
    file.write("              " + str(cube[16, 0:3]) + '\n')
    file.write("              " + str(cube[17, 0:3]) + '\n')

    return True


# checks if child ascendant of parent
def contains1(child, parent):
    curr = parent.parent
    while curr is not None:
        if np.array_equal(curr.cube, child): return True
        curr = curr.parent

    return False


# checks if frontier contains child
def contains2(child, frontier):
    for curr in frontier:
        if np.array_equal(curr.cube, child): return True

    return False


def idfs(start):
    cost_limit = 6
    nodes = 0
    frontier = list()
    branching_factors = list()

    while True:
        frontier.append(start)

        while len(frontier) != 0:
            curr = frontier.pop()

            if goal_reached(curr.cube):
                print('Goal Height:', curr.cost)
                print("Nodes Generated:", nodes)
                return

            if curr.cost + 1 <= cost_limit:
                child_cost = curr.cost + 1
                b = 0
                for i in range(12):
                    nodes = nodes + 1
                    new = State()
                    new.cube = np.array(curr.cube)
                    new.cost = child_cost
                    new.parent = curr
                    new.move = make_move(new.cube, i + 1, 0)
                    # if curr.parent is not None and np.array_equal(curr.parent.cube, new.cube):
                    if curr.parent is not None and (contains1(new.cube, curr) or contains2(new.cube, frontier)):
                        continue
                    frontier.append(new)
                    b = b + 1
                branching_factors.append(b)

        branching_factors.clear()

##########################################


curr = State()
curr.cube = np.array(xInitial)
handle = open('input3.txt')
indexes = [0, 1, 2, 3, 6, 9, 12, 4, 7, 10, 13, 5, 8, 11, 14, 15, 16, 17]
index = 0
for line in handle:
    line = line.replace(' ', '')
    for row in line.split('['):
        if len(row) != 0:
            i = indexes[index]
            curr.cube[i, 0] = row[1]
            curr.cube[i, 1] = row[4]
            curr.cube[i, 2] = row[7]
            index = index + 1

time.ctime()
fmt = '%H:%M:%S'
start = time.strftime(fmt)

idfs(curr)

time.ctime()
end = time.strftime(fmt)
print("Time taken(sec):", datetime.strptime(end, fmt) - datetime.strptime(start, fmt))

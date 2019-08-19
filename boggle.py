from random import choice
from string import ascii_uppercase
import logging
import time
# logging.basicConfig(level=logging.INFO)

def timeit(method):
    """Calculates time taken to run a function when called"""

    def timed(*args, **kw):
        t1 = time.time()
        result = method(*args, **kw)
        print('%r %2.2f sec' % (method.__name__, time.time() - t1))
        return result

    return timed


def get_grid():
    """Return a dictionary of grid positions to random letters"""
    """abbreviate"""
    return {
        (0, 0): 'A', (1, 0): 'C', (2, 0): 'E',
        (0, 1): 'D', (1, 1): 'O', (2, 1): 'S',
        (0, 2): 'D', (1, 2): 'U', (2, 2): 'T'

    }


# (0, 0): 'C', (1, 0): 'O', (2, 0): 'S', (3, 0): 'S',
# (0, 1): 'N', (1, 1): 'O', (2, 1): 'S', (3, 1): 'R',
# (0, 2): 'D', (1, 2): 'U', (2, 2): 'T', (3, 2): 'R',
# (0, 3): 'B', (1, 3): 'B', (2, 3): 'Y', (3, 3): 'R',

def get_grid_2():
    """Return a dictionary of grid positions to random letters"""
    return {(x, y): choice(ascii_uppercase) for x in range(X) for y in range(Y)}


def get_neighbours():
    """Return a dictionary with all the neighbours surrounding a particular position"""
    neighbours = {}

    for position in grid:
        x, y = position
        positions = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
            (x, y + 1),
            (x - 1, y + 1),
            (x - 1, y)
        ]

        # smth = [p for p in positions if 0 <= p[0] < X and 0 <= p[1] < Y and p[0] == position[0]]
        nbr = [p for p in positions if 0 <= p[0] < X and 0 <= p[1] < Y]
        # print('position: ' + str(position))
        # print('соседи: ' + str(nbr))
        # print('----------')
        neighbours[position] = nbr
    return neighbours


def path_to_word(path):
    """Convert a list of grid positions to a word"""
    return ''.join([grid[p] for p in path])


def search(path):
    """Recursively search the grid for words"""
    word = path_to_word(path)
    logging.debug('%s: %s' % (path, word))
    if word not in stems:
        return
    if word in dictionary:
        if is_valid_path(path):
            paths.append(path)
    for next_pos in neighbours[path[-1]]:

        if next_pos not in path:
            # if is_valid_path(path + [next_pos]):
            search(path + [next_pos])
    else:
        logging.debug('skipping %s because in path' % grid[next_pos])


def is_valid_path(path):
    first_element = path[0]
    horizontal = all(item[1] == first_element[1] for item in path)
    vertical = all(item[0] == first_element[0] for item in path)
    diagonal = is_valid_diagonal(path)
    result = horizontal or vertical or diagonal

    return result


def get_dictionary():
    """Return a list of uppercase english words, including word stems"""
    stems, dictionary = set(), set()
    with open('words.txt') as f:
        for word in f:
            word = word.strip().upper()
            dictionary.add(word)

            for i in range(len(word)):
                stems.add(word[:i + 1])

    return dictionary, stems


@timeit
def get_words():
    """Search each grid position and return all the words found"""
    for position in grid:
        logging.info('searching %s' % str(position))
        # print(str(position))
        search([position])
    return [path_to_word(p) for p in paths]


def print_grid(grid):
    """Print the grid as a readable string"""
    s = ''
    for y in range(Y):
        for x in range(X):
            s += grid[x, y] + ' '
        s += '\n'
    print(s)


# my custom grid
# size = X, Y = 3, 3
# grid = get_grid()
# production ready grid

size = X, Y = 15, 15
grid = get_grid_2()

neighbours = get_neighbours()


def check_if_axis_valid(axis):
    path_length = len(axis)
    if path_length <= 2:
        return False
    is_axes_valid = True
    if axis[path_length - 1] < axis[0]:
        axis = list(reversed(axis))
    for i in range(path_length):
        if i < path_length - 1:
            if axis[i + 1] > axis[i] and axis[i + 1] - axis[i] == 1:
                continue
            else:
                is_axes_valid = False
                break
    return is_axes_valid


def is_valid_diagonal(path):
    axis_x = list([s[0] for s in path])
    axis_y = list([s[1] for s in path])
    a = check_if_axis_valid(axis_x)
    if not a:
        return False
    b = check_if_axis_valid(axis_y)
    return a and b


dictionary, stems = get_dictionary()
paths = []

print_grid(grid)
words = get_words()
print(words)
print(paths)
print('word size: ' + str(len(words)))
print('path size: ' + str(len(paths)))


# ['ACE', 'AD', 'ADD', 'ES', 'DO', 'DOS', 'SO', 'SOD', 'DOE', 'TS']
# A C E
# D O S
# D U T

# W R H J D
# N G C H C
# C E K K Z
# S N X B Z
# K E F T A
# ['NEXT', 'CS', 'KS', 'GENE', 'KC', 'AT']

# H W U G
# T K W Q
# V S R O
# H N G W
# ['VS', 'KS', 'RS', 'OW', 'OR']

# E X W P
# U H E E
# N M D K
# E B S K
#
# 'get_words' 0.01 sec
# ['EX', 'UH', 'NU', 'HE', 'BE', 'WE', 'WED', 'WEDS', 'EH', 'DEW', 'KS']

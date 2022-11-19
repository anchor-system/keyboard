from typing import Tuple

import constants


def two_dimensional_list_to_string(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = "\t".join("{{:{}}}".format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return "\n".join(table)


def center_point(p: Tuple):
    x, y = p[0], p[1]
    return (x + constants.WIDTH / 2, y + constants.HEIGHT / 2)

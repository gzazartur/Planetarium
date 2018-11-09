"""
The Calculation class to calculate the positions
"""
import json
import numpy
import scipy.constants as s_con
import matplotlib.pyplot as plt


def open_json():
    """
    The open_json load the json data from the src directory
    :return: A dictionary of the orb data
    """
    with open('orbs.json', 'r') as f:
        orb_dict = json.load(f)
    return orb_dict


GRAVITATION = s_con.G


class Calculation:

    def __init__(self):
        self.step_wide = int(input("Schrittweite: "))
        self.num_orbs = len(open_json())
        self.orbs = open_json()
        self.pos = [0, 0]

    @staticmethod
    def distance(orb2, orb1):
        """
        Calculate the distance between two coordinates
        :param orb2: the position of the Orb2
        :param orb1: the position ot the Orb1
        :return: the distance
        """
        distance = numpy.sqrt(((orb2[0] - orb1[0]) ** 2) +
                              ((orb2[1] - orb1[1]) ** 2))
        return distance

    def calculate_acceleration(self, orb1_index):
        """
        Calculate the acceleration of one Orb
        :param orb1_index: the Orb which will be calculated
        :return: the acceleration
        """
        orb1_pos = self.orbs[orb1_index]["Pos"]
        orb1_mass = self.orbs[orb1_index]["Mass"] * (10 ** 7)
        orbs_without_orb1 = self.orbs[:orb1_index] + self.orbs[orb1_index + 1:]

        orb1_force = 0

        for orb in orbs_without_orb1:
            orb2_pos = orb["Pos"]
            distance = self.distance(orb2_pos, orb1_pos)
            mass = orb1_mass * orb["Mass"] * (10 ** 7)
            orb1_force += GRAVITATION * (mass / numpy.fabs(distance ** 3)) * distance

        acceleration = orb1_force / orb1_mass

        return acceleration

    def delta_t(self):
        delta_t = 4
        return delta_t

    def calculate_universe_new_positions(self, steps):
        positions = list()
        for _ in range(steps):
            positions.append(self.calculate_object_new_position(1))

        return positions

    def calculate_object_new_position(self, orb_index):
        acceleration = self.calculate_acceleration(orb_index)
        velocity = self.orbs[orb_index]["Velocity"]
        delta_t = self.delta_t()

        x_new_pos = numpy.multiply(delta_t, velocity)
        y_new_pos = numpy.divide((delta_t ** 2), 2) * acceleration

        orb_pos2 = [x_new_pos, y_new_pos]

        new_orb_pos = list(map(lambda x, y: x + y, orb_pos2, self.pos))

        self.pos = new_orb_pos

        return new_orb_pos


if __name__ == '__main__':
    c = Calculation()

    coord_list = c.calculate_universe_new_positions(c.step_wide)
    x = list()
    y = list()

    for coord in coord_list:
        x.append(coord[0])
        y.append(coord[1])
    plt.scatter(x, y)
    plt.show()
    print(c.calculate_universe_new_positions(c.step_wide))

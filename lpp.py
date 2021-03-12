# -*- coding: utf-8 -*-
"""
Created on Fri Feb ? 13:13:13 2021

@author: Reuel R. D'silva
"""

# Imports
import re
import numpy as np

from scipy import linalg
from constraint import Constraint
from itertools import combinations

from utils import parse_equation

class LPP:
    """A Class used to represent a Linear Programming Problem

    The solve method can be used to find intersection points,
    corner points of the fesiable region and calculate the
    objective function.

    An example of a Linear Programming Problem:
        Maximize: z = 5x_1 + 4x_2
        Subject to:
            6x_1 + 4x_2 <= 24
            x_1 + 2x_2 <= 6
            -x_1 + x_2 <= 1
            x_2 <= 2
            x_1 >= 0
            x_2 >= 0

    Attributes
    ----------

        obj_var: str
            Objective Variable.
            (for the example above, the obj_var will be z)

        obj_fn: str
            The Objective function represented as a string
            (for the example above, the obj_fn will be 5x_1 + 4x_2)

        X: list[str]
            X represents the variables.
            (for the example above, X will be ["x_1", "x_2"])

        c: NumPy Array
            A vector of coefficients of the objective function
            with size (number_of_variables).

            (for the example above, c will be [5 4])

        problem_type: str
            A String that indicates the type of the LPP.
            It can either be "maximize" or "minimize"

        constraints: list
            It is a list of constraint objects.

        intersection_points: list
            The interection points of the constraints where each point
            is represented as a vector.

        corner_points: list
            The list of corner points of the Feasible Region

        sol_point: NumPy Array
            The point at which the LPP is maximized or minimized

        z: float
            The solution of the LPP
        
        z_values: list
            list of value of the objective function as float
            at each Corner Point.

    """
    def __init__(self, objective, constraints):
        """Initialize LPP

        Parameters
        ----------
        objective : string
            The objective function of the LPP.
        constraints : list
            The constraints of the LPP as a list of strings

        """

        # Parse the first line of the LPP
        # Eg: Maximize: z = 5x1 + 4x2
        #   problem_type = Maximize
        #   obj_var = z
        #   obj_fn = 5x1 + 4x2
        problem_type, self.obj_var, self.obj_fn = re.split(
            r":|=",
            objective,
        )

        c, self.X = parse_equation(self.obj_fn)
        self.constraints = self.parse_constraints(constraints)

        self.c = np.array(c)
        self.problem_type = problem_type.lower()

        self.intersection_points = []
        self.corner_points = []
        self.sol_point = None
        self.z_values = []

        if self.problem_type == "maximize":
            self.z = 0
        else:
            self.z = np.inf


    def parse_constraints(self, constraints):
        """Parse the string Constraint into Constraint Object


        Parameters
        ----------
        constraints : list
            The constraints of the LPP as a list of strings

        Returns
        -------
        constraints_array : list
            The constraints of the LPP as a list of Constraint Objects

        """
        constraints_array = []

        for constraint in constraints:

            parsed_constraint = Constraint(constraint, self.X)
            constraints_array.append(parsed_constraint)

        return constraints_array


    def solve(self):
        """Solve the LPP

        The solve method first finds the Intersection Points. It then
        evaluates each of the intersection points against all the
        constraints to get a list of Corner Points of the Feasible Region.

        Finally, it evaluates the objective function using all the Corner
        Points and finds the solution to the LPP.

        """
        
        # Pick choose number_of_variables constraints find intersection points.
        # i.e. if number_of_variables = 2, pick 2 constraints at a time.
        #      if number_of_variables = 5, pick 5 constraints at a time.
        for constraints in combinations(self.constraints, len(self.X)):

            coeffs = [constraint.A for constraint in constraints]
            b = [constraint.b for constraint in constraints]

            A = np.vstack(coeffs)
            b = np.vstack(b)

            try:
                X = linalg.solve(A, b)
                self.intersection_points.append(X)

            # LinAlgError happens when the lines are Parallel. 
            # So we just ignore it and move on
            except linalg.LinAlgError:
                pass

        # Find corner points
        for point in self.intersection_points:
            for constraint in self.constraints:
                if not constraint.satisfies(point):
                    break
            else:
                self.corner_points.append(point)

        # Find value of objective function at each corner point
        for point in self.corner_points:
            z = round(float(self.c.dot(point)),2)
            self.z_values.append(z)

            if self.problem_type == "maximize" and z > self.z:
                self.z = z
                self.sol_point = point
            elif self.problem_type == "minimize" and z < self.z:
                self.z = z
                self.sol_point = point

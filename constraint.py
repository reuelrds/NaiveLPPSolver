# -*- coding: utf-8 -*-
"""
Created on Fri Feb ? 13:09:50 2021

@author: Reuel R. D'silva'
"""

# Imports
import re
from equation import Equation

class Constraint(Equation):
    """Used to represent constraints in a LPP
    The class inherites the Equation class


    Attributes
    ----------
        sign_type: str
            Type of constraint. It can either be >= or <= or =
        constraint_str: str
            The constraint in string format.
    """
    def __init__(self, constraint, variables):
        """Initialize Constraint class

        Parameters
        ----------
        constraint : str
            The constraint of an LPP in string format.
            e.g. 5x1 + 6x2 - 2x3 >= 4
        variables : list[str]
            Variables of the constraint as list of strings.
            e.g. ["x1", "x2", "x3"]

        """
        
        # Splits the constraint.
        # eg: 6x1 + 4x2 <= 24
        #   lhs: 6x1 + 4x2
        #   sign_type: <=
        #   rhs: 24
        lhs, self.sign_type, rhs = re.split(
            r"(>=|=|<=)",
            constraint
        )

        self.constraint_str = constraint
        super().__init__(lhs, variables, rhs)


    def satisfies(self, point):
        """Checks whether a point satisfies a constraint.


        Parameters
        ----------
        point : Numpy Array
            A Point represented as a vector.

        Returns
        -------
        boolean
            Returns True if the point satisfies the equation
            else returns False.
        """
        
        # Rounding off because error were cause while testing due to
        # floating point error.
        # eg: for 6x1 + 4x2 <= 24
        #       At x1 = 3 & x2 = 1.5 
        #       the value always turned out to be 24.00000000000000005
        #       But if manually calculated we know it should be exactly 24.0
        z = round(float(self.A.dot(point)),2)

        if self.sign_type == "<=":
            satisfies = z <= self.b
        elif self.sign_type == ">=":
            satisfies = z >= self.b
        else:
            satisfies = z == self.b

        return satisfies


    def __str__(self):
        """Returns String representation of the constraint.

        The methods gets called when the constraint is printed to console.
        eg. print(constraint)

        Returns
        -------
        str
            String representation of the constraint.

        """
        return self.constraint_str
